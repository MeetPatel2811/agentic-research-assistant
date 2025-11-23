# This module defines the WriterAgent, which converts analysis results
# into a nicely formatted markdown response for the user.

from typing import Dict, List

from tools.built_in.formatter_tool import format_markdown_response
from memory.memory_manager import MemoryManager
from utils.logger import log_info


class WriterAgent:
    # This class represents an agent specialized in response generation/formatting.
    def __init__(self, memory: MemoryManager) -> None:
        self.memory = memory

    def run(self, query: str, analysis: Dict[str, object], sources: List[Dict[str, str]]) -> str:
        # This method formats the final answer to be shown to the user.
        log_info("WriterAgent: starting writing step")

        summary = str(analysis.get("summary", ""))
        claims: List[str] = list(analysis.get("claims", []))  # type: ignore[arg-type]
        evidence: List[str] = list(analysis.get("evidence", []))  # type: ignore[arg-type]

        response = format_markdown_response(
            query=query,
            summary=summary,
            claims=claims,
            evidence=evidence,
            sources=sources,
        )

        # This stores the final response to memory as part of the conversation history.
        self.memory.add_conversation(query=query, response=response)
        log_info("WriterAgent: writing step completed")
        return response
