# This module implements a simple built-in "web search" style tool.
# For offline use, it searches over a small in-memory corpus of documents.

from typing import List, Dict
from utils.logger import log_info


# This is a tiny in-memory "corpus" that simulates web documents.
CORPUS: List[Dict[str, str]] = [
    {
        "title": "Introduction to Agentic AI Systems",
        "content": (
            "Agentic AI systems use autonomous agents that can plan, act, "
            "and collaborate. They often include a controller, memory, and tools."
        ),
    },
    {
        "title": "Multi-Agent Orchestration Basics",
        "content": (
            "Multi-agent orchestration coordinates multiple specialized agents. "
            "A controller delegates tasks, and agents use tools to complete subtasks."
        ),
    },
    {
        "title": "Reinforcement Learning for Improvement",
        "content": (
            "Reinforcement learning can be used to improve an agent's behavior over time. "
            "Feedback signals can adjust strategies or prompt configurations."
        ),
    },
    {
        "title": "Fact-Checking in Research Assistants",
        "content": (
            "Research assistants should cross-check sources, extract claims, "
            "and map evidence to those claims for improved reliability."
        ),
    },
]


def simple_keyword_score(query: str, text: str) -> int:
    # This helper function scores how many query words appear in a given text.
    query_words = [w.lower() for w in query.split() if len(w) > 2]
    text_lower = text.lower()
    return sum(1 for w in query_words if w in text_lower)


def web_search(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    # This function performs a simple keyword-based search over the CORPUS.
    log_info(f"WebSearchTool: searching for '{query}'")
    scored_docs = []
    for doc in CORPUS:
        score = simple_keyword_score(query, doc["content"] + " " + doc["title"])
        scored_docs.append((score, doc))
    # Sort by score descending and take top_k
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    results = [doc for score, doc in scored_docs if score > 0][:top_k]
    log_info(f"WebSearchTool: found {len(results)} relevant documents")
    return results
