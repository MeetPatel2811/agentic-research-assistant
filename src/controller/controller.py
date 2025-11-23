# This module defines the main Controller class,
# which orchestrates the multi-agent workflow.

from typing import Dict, Any, List

from controller.protocol import AgentMessage, ControllerDecision
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.writer_agent import WriterAgent
from rl.feedback_loop import evaluate_response_quality, should_retry
from utils.logger import log_info, log_error
from utils.validators import validate_query


class Controller:
    # This class represents the central controller for orchestrating agents.
    def __init__(
        self,
        research_agent: ResearchAgent,
        analysis_agent: AnalysisAgent,
        writer_agent: WriterAgent,
    ) -> None:
        self.research_agent = research_agent
        self.analysis_agent = analysis_agent
        self.writer_agent = writer_agent

    def _decide_next_agent(self, step: str) -> ControllerDecision:
        # This private method implements a simple decision policy
        # about which agent should run for the current step.
        if step == "research":
            return ControllerDecision(
                next_agent="research",
                reason="Need to gather relevant information from sources.",
                metadata={},
            )
        elif step == "analysis":
            return ControllerDecision(
                next_agent="analysis",
                reason="Need to summarize and extract claims/evidence.",
                metadata={},
            )
        else:
            return ControllerDecision(
                next_agent="writer",
                reason="Need to format final answer for the user.",
                metadata={},
            )

    def handle_query(self, query: str) -> str:
        # This method handles a full query by coordinating all agents,
        # including a feedback loop that may trigger a retry.
        log_info(f"Controller: received query: {query}")

        # This validates the query and returns early on invalid input.
        if not validate_query(query):
            log_error("Controller: invalid query provided")
            return "Your query appears to be empty. Please provide a meaningful question."

        # Step 1: Research
        decision = self._decide_next_agent("research")
        log_info(f"Controller decision: {decision.reason}")
        research_msg = AgentMessage(
            sender="controller",
            receiver="research_agent",
            task_type="research",
            payload={"query": query},
        )
        sources = self._handle_research(research_msg)

        # Step 2: Analysis
        decision = self._decide_next_agent("analysis")
        log_info(f"Controller decision: {decision.reason}")
        analysis_msg = AgentMessage(
            sender="controller",
            receiver="analysis_agent",
            task_type="analysis",
            payload={"query": query, "sources": sources},
        )
        analysis = self._handle_analysis(analysis_msg)

        # Step 3: Writing
        decision = self._decide_next_agent("writer")
        log_info(f"Controller decision: {decision.reason}")
        writer_msg = AgentMessage(
            sender="controller",
            receiver="writer_agent",
            task_type="write",
            payload={"query": query, "analysis": analysis, "sources": sources},
        )
        response = self._handle_writer(writer_msg)

        # Step 4: Feedback Loop
        quality = evaluate_response_quality(analysis, response)
        if should_retry(quality):
            log_info("Controller: retrying analysis and writing due to low quality score")
            # Retry analysis with same sources but maybe different emphasis (simplified here)
            analysis = self._handle_analysis(analysis_msg)
            response = self._handle_writer(writer_msg)

        log_info("Controller: finished handling query")
        return response

    def _handle_research(self, msg: AgentMessage) -> List[Dict[str, Any]]:
        # This private method handles the research step by calling the ResearchAgent.
        query = msg.payload.get("query", "")
        sources = self.research_agent.run(query=query, top_k=3)
        return sources

    def _handle_analysis(self, msg: AgentMessage) -> Dict[str, Any]:
        # This private method handles the analysis step by calling the AnalysisAgent.
        query = msg.payload.get("query", "")
        sources = msg.payload.get("sources", [])
        analysis = self.analysis_agent.run(query=query, sources=sources)
        return analysis

    def _handle_writer(self, msg: AgentMessage) -> str:
        # This private method handles the writing step by calling the WriterAgent.
        query = msg.payload.get("query", "")
        analysis = msg.payload.get("analysis", {})
        sources = msg.payload.get("sources", [])
        response = self.writer_agent.run(query=query, analysis=analysis, sources=sources)
        return response
