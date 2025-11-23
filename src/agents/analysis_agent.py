# This module defines the AnalysisAgent, which summarizes sources
# and uses the custom claim/evidence extractor tool.

from typing import Dict, List

from tools.built_in.summarizer_tool import summarize_documents
from tools.custom.claim_evidence_extractor import extract_claims_and_evidence
from memory.memory_manager import MemoryManager
from utils.logger import log_info


class AnalysisAgent:
    # This class represents an agent specialized in analyzing gathered information.
    def __init__(self, memory: MemoryManager) -> None:
        self.memory = memory

    def run(self, query: str, sources: List[Dict[str, str]]) -> Dict[str, object]:
        # This method summarizes sources and extracts claims and evidence.
        log_info("AnalysisAgent: starting analysis step")
        summary = summarize_documents(sources)
        extraction = extract_claims_and_evidence(summary)
        # This stores the main claims as "facts" for future context.
        for c in extraction.get("claims", []):
            self.memory.add_fact(c, source="analysis_summary")

        analysis_result: Dict[str, object] = {
            "query": query,
            "summary": summary,
            "claims": extraction.get("claims", []),
            "evidence": extraction.get("evidence", []),
            "confidence": extraction.get("confidence", 0.0),
        }
        log_info(
            f"AnalysisAgent: analysis done with {len(analysis_result['claims'])} claims "
            f"and confidence {analysis_result['confidence']}"
        )
        return analysis_result
