# This module defines the ResearchAgent, responsible for finding
# relevant documents using the web_search tool and using memory.

from typing import List, Dict

from tools.built_in.web_search_tool import web_search
from memory.memory_manager import MemoryManager
from utils.logger import log_info


class ResearchAgent:
    # This class represents an agent specialized in information retrieval.
    def __init__(self, memory: MemoryManager) -> None:
        self.memory = memory

    def run(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        # This method executes the research step using the web_search tool.
        log_info("ResearchAgent: starting research step")
        results = web_search(query, top_k=top_k)
        # This stores brief "facts" about which titles were consulted.
        for r in results:
            title = r.get("title", "Untitled Source")
            self.memory.add_fact(f"Consulted source: {title}", source=title)
        log_info(f"ResearchAgent: completed with {len(results)} results")
        return results
