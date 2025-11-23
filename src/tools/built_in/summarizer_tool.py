# This module provides a simple summarization tool.
# It compresses a list of documents into a short textual summary.

from typing import List, Dict


def summarize_documents(documents: List[Dict[str, str]], max_sentences: int = 4) -> str:
    # This function summarizes multiple documents by joining key sentences.
    # For simplicity, we just take the first couple of sentences from each document.
    if not documents:
        return "No relevant documents were found to summarize."

    sentences: List[str] = []
    for doc in documents:
        content = doc.get("content", "")
        # Naive sentence splitting on period.
        raw_sentences = [s.strip() for s in content.split(".") if s.strip()]
        # Take up to 2 sentences from each document.
        sentences.extend(raw_sentences[:2])

    # Truncate to the global limit of sentences in the final summary.
    sentences = sentences[:max_sentences]
    summary = ". ".join(sentences)
    if not summary.endswith("."):
        summary += "."
    return summary
