# This module defines a custom tool for extracting claims and evidence
# from a chunk of text. This is your "custom tool" for the assignment.

from typing import Dict, List


def extract_claims_and_evidence(text: str) -> Dict[str, object]:
    # This function naively classifies sentences into "claims" and "evidence".
    # It returns a dictionary containing claims, evidence, and a simple confidence measure.
    if not text or not isinstance(text, str):
        return {"claims": [], "evidence": [], "confidence": 0.0}

    sentences = [s.strip() for s in text.split(".") if s.strip()]
    claim_keywords = ["is", "are", "will", "can", "should", "must"]
    claims: List[str] = []
    evidence: List[str] = []

    for s in sentences:
        # Very simple heuristic: if a sentence contains a claim word, treat it as a claim.
        # Otherwise, treat it as supporting evidence.
        if any(f" {kw} " in s.lower() for kw in claim_keywords):
            claims.append(s)
        else:
            evidence.append(s)

    # Simple "confidence": fraction of sentences we categorized as claims or evidence.
    total = len(sentences)
    classified = len(claims) + len(evidence)
    confidence = classified / total if total > 0 else 0.0

    return {"claims": claims, "evidence": evidence, "confidence": round(confidence, 2)}
