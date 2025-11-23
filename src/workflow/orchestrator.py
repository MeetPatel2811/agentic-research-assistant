# This module defines the Orchestrator, which wires together
# memory, agents, and controller for a single end-to-end workflow.

from memory.memory_manager import MemoryManager
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.writer_agent import WriterAgent
from controller.controller import Controller
from utils.logger import log_info


class Orchestrator:
    # This class is a simple façade that sets up and runs the agentic workflow.
    def __init__(self) -> None:
        # This builds shared memory and agent instances.
        self.memory = MemoryManager()
        self.research_agent = ResearchAgent(memory=self.memory)
        self.analysis_agent = AnalysisAgent(memory=self.memory)
        self.writer_agent = WriterAgent(memory=self.memory)
        self.controller = Controller(
            research_agent=self.research_agent,
            analysis_agent=self.analysis_agent,
            writer_agent=self.writer_agent,
        )

    def run(self, query: str) -> str:
        # This method executes the full pipeline for a given user query.
        log_info("Orchestrator: starting pipeline")
        response = self.controller.handle_query(query)
        log_info("Orchestrator: pipeline finished")
        return response
