from typing import List, Dict
from utils.logger import log_info, log_error

# Try to import DuckDuckGo, fallback to corpus
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
    log_info("DuckDuckGo search available")
except ImportError:
    DDGS_AVAILABLE = False
    log_error("DuckDuckGo not installed. Using fallback corpus search.")


# Keep the original corpus for fallback
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


def web_search_duckduckgo(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    """Search using DuckDuckGo (real web search)."""
    try:
        log_info(f"DuckDuckGo: searching for '{query}'")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=top_k))
        
        # Format results to match our schema
        formatted_results = []
        for r in results:
            formatted_results.append({
                "title": r.get("title", "Untitled"),
                "content": r.get("body", "No content available."),
                "url": r.get("href", "")
            })
        
        log_info(f"DuckDuckGo: found {len(formatted_results)} results")
        return formatted_results
    
    except Exception as e:
        log_error(f"DuckDuckGo search failed: {e}")
        return []


def simple_keyword_score(query: str, text: str) -> int:
    """Score how many query words appear in text."""
    query_words = [w.lower() for w in query.split() if len(w) > 2]
    text_lower = text.lower()
    return sum(1 for w in query_words if w in text_lower)


def web_search_corpus(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    """Fallback: search in local corpus."""
    log_info(f"Corpus search: searching for '{query}'")
    scored_docs = []
    for doc in CORPUS:
        score = simple_keyword_score(query, doc["content"] + " " + doc["title"])
        scored_docs.append((score, doc))
    
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    results = [doc for score, doc in scored_docs if score > 0][:top_k]
    log_info(f"Corpus search: found {len(results)} documents")
    return results


def web_search(query: str, top_k: int = 3, use_real_search: bool = True) -> List[Dict[str, str]]:
    """
    Main web search function.
    Tries DuckDuckGo first, falls back to corpus if unavailable or fails.
    """
    if use_real_search and DDGS_AVAILABLE:
        results = web_search_duckduckgo(query, top_k)
        if results:  # If we got results, return them
            return results
        else:
            log_info("DuckDuckGo returned no results, falling back to corpus")
    
    # Fallback to corpus
    return web_search_corpus(query, top_k)