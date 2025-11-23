
import time
from typing import Dict, Any, List, Optional

from controller.protocol import AgentMessage, ControllerDecision
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.writer_agent import WriterAgent
from rl.feedback_loop import evaluate_response_quality, should_retry
from utils.logger import log_info, log_error  
from utils.validators import validate_query

class Controller:
    def __init__(
        self,
        research_agent: ResearchAgent,
        analysis_agent: AnalysisAgent,
        writer_agent: WriterAgent,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> None:
        self.research_agent = research_agent
        self.analysis_agent = analysis_agent
        self.writer_agent = writer_agent
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _handle_research_with_retry(self, msg: AgentMessage) -> List[Dict[str, Any]]:
        """Execute research with automatic retry on failure."""
        query = msg.payload.get("query", "")
        
        for attempt in range(self.max_retries):
            try:
                log_info(f"Research attempt {attempt + 1}/{self.max_retries}")
                sources = self.research_agent.run(query=query, top_k=3)
                
                if not sources or len(sources) == 0:
                    raise ValueError("No sources returned from research agent")
                
                return sources
                
            except Exception as e:
                log_error(f"Research failed on attempt {attempt + 1}: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    log_info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    log_error("Research failed after all retries. Using fallback.")
                    # Fallback: return minimal context
                    return [{
                        "title": "System Notice",
                        "content": f"Unable to retrieve sources for query: {query}. Using cached knowledge."
                    }]

    def _handle_analysis_with_retry(self, msg: AgentMessage) -> Dict[str, Any]:
        """Execute analysis with automatic retry on failure."""
        query = msg.payload.get("query", "")
        sources = msg.payload.get("sources", [])
        
        for attempt in range(self.max_retries):
            try:
                log_info(f"Analysis attempt {attempt + 1}/{self.max_retries}")
                analysis = self.analysis_agent.run(query=query, sources=sources)
                
                # Validate analysis output
                if not isinstance(analysis, dict):
                    raise ValueError("Analysis returned invalid format")
                
                if "summary" not in analysis:
                    raise ValueError("Analysis missing required 'summary' field")
                
                return analysis
                
            except Exception as e:
                log_error(f"Analysis failed on attempt {attempt + 1}: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    # Fallback: basic analysis
                    log_error("Analysis failed. Using fallback analysis.")
                    return {
                        "query": query,
                        "summary": "Analysis could not be completed. Please try a different query.",
                        "claims": [],
                        "evidence": [],
                        "confidence": 0.0
                    }

    def _handle_writer_with_retry(self, msg: AgentMessage) -> str:
        """Execute writer with automatic retry on failure."""
        for attempt in range(self.max_retries):
            try:
                log_info(f"Writer attempt {attempt + 1}/{self.max_retries}")
                response = self.writer_agent.run(
                    query=msg.payload.get("query", ""),
                    analysis=msg.payload.get("analysis", {}),
                    sources=msg.payload.get("sources", [])
                )
                
                if not response or len(response.strip()) < 50:
                    raise ValueError("Writer returned insufficient content")
                
                return response
                
            except Exception as e:
                log_error(f"Writer failed on attempt {attempt + 1}: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    return "# System Error\n\nUnable to generate response. Please try again."

    def handle_query(self, query: str) -> str:
        """Handle query with comprehensive error recovery."""
        log_info(f"Controller: received query: {query}")

        try:
            # Validate query
            if not validate_query(query):
                log_error("Controller: invalid query provided")
                return "Your query appears to be empty. Please provide a meaningful question."

            # Step 1: Research with retry
            research_msg = AgentMessage(
                sender="controller",
                receiver="research_agent",
                task_type="research",
                payload={"query": query},
            )
            sources = self._handle_research_with_retry(research_msg)

            # Step 2: Analysis with retry
            analysis_msg = AgentMessage(
                sender="controller",
                receiver="analysis_agent",
                task_type="analysis",
                payload={"query": query, "sources": sources},
            )
            analysis = self._handle_analysis_with_retry(analysis_msg)

            # Step 3: Writing with retry
            writer_msg = AgentMessage(
                sender="controller",
                receiver="writer_agent",
                task_type="write",
                payload={"query": query, "analysis": analysis, "sources": sources},
            )
            response = self._handle_writer_with_retry(writer_msg)

            # Step 4: Quality check and potential retry
            quality = evaluate_response_quality(analysis, response)
            if should_retry(quality):
                log_info("Controller: Low quality detected, attempting improvement")
                # One more attempt with refined analysis
                analysis = self._handle_analysis_with_retry(analysis_msg)
                response = self._handle_writer_with_retry(writer_msg)

            log_info("Controller: Successfully completed query")
            return response

        except Exception as e:
            log_error(f"Critical error in controller: {str(e)}")
            return f"# System Error\n\nAn unexpected error occurred: {str(e)}\nPlease try again or contact support."

    # Keep old methods but mark as deprecated
    def _handle_research(self, msg: AgentMessage) -> List[Dict[str, Any]]:
        return self._handle_research_with_retry(msg)
    
    def _handle_analysis(self, msg: AgentMessage) -> Dict[str, Any]:
        return self._handle_analysis_with_retry(msg)
    
    def _handle_writer(self, msg: AgentMessage) -> str:
        return self._handle_writer_with_retry(msg)