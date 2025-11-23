# This module contains a formatting tool to convert analysis output
# into a structured, user-friendly markdown response.

from typing import Dict, List


def format_markdown_response(
    query: str,
    summary: str,
    claims: List[str],
    evidence: List[str],
    sources: List[Dict[str, str]],
) -> str:
    # This function builds a markdown-formatted response including
    # the summary, extracted claims, evidence, and sources.
    lines: List[str] = []
    lines.append(f"# Research Summary for: **{query}**\n")
    lines.append("## Overview\n")
    lines.append(summary + "\n")

    if claims:
        lines.append("## Key Claims\n")
        for idx, c in enumerate(claims, start=1):
            lines.append(f"{idx}. {c}")
        lines.append("")

    if evidence:
        lines.append("## Supporting Evidence\n")
        for idx, e in enumerate(evidence, start=1):
            lines.append(f"{idx}. {e}")
        lines.append("")

    if sources:
        lines.append("## Sources Consulted\n")
        for idx, s in enumerate(sources, start=1):
            title = s.get("title", "Untitled Source")
            lines.append(f"- {idx}. {title}")
        lines.append("")

    return "\n".join(lines)
