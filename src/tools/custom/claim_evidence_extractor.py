from typing import Dict, List
import spacy
from utils.logger import log_info, log_error

# Load spaCy model (do this once at module level)
try:
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
    log_info("SpaCy model loaded successfully")
except Exception as e:
    log_error(f"SpaCy not available: {e}. Falling back to keyword-based extraction.")
    SPACY_AVAILABLE = False


def extract_claims_and_evidence_advanced(text: str) -> Dict[str, object]:
    """
    Advanced claim and evidence extraction using spaCy NLP.
    Falls back to keyword-based if spaCy unavailable.
    """
    if not text or not isinstance(text, str):
        return {"claims": [], "evidence": [], "confidence": 0.0}

    if not SPACY_AVAILABLE:
        return extract_claims_and_evidence_fallback(text)

    try:
        doc = nlp(text)
        claims: List[str] = []
        evidence: List[str] = []
        
        # Analyze each sentence
        for sent in doc.sents:
            sent_text = sent.text.strip()
            if len(sent_text) < 10:  # Skip very short sentences
                continue
            
            # Extract root verb and check for assertive patterns
            root = sent.root
            is_claim = False
            is_evidence = False
            
            # Claim indicators: root verb is assertive
            assertive_verbs = {"is", "are", "was", "were", "can", "will", "should", 
                             "must", "demonstrates", "shows", "indicates", "suggests"}
            
            if root.lemma_ in assertive_verbs or root.pos_ == "VERB":
                # Check for modal verbs (claims)
                has_modal = any(token.pos_ == "AUX" for token in sent)
                has_subject = any(token.dep_ in ["nsubj", "nsubjpass"] for token in sent)
                
                if has_modal or has_subject:
                    is_claim = True
            
            # Evidence indicators: contains numbers, citations, or references
            has_numbers = any(token.like_num or token.pos_ == "NUM" for token in sent)
            has_citation = any(token.text.lower() in ["study", "research", "according", "found"] 
                             for token in sent)
            
            if has_numbers or has_citation:
                is_evidence = True
            
            # Categorize
            if is_claim and not is_evidence:
                claims.append(sent_text)
            elif is_evidence:
                evidence.append(sent_text)
            elif is_claim:  # Both claim and evidence
                claims.append(sent_text)
        
        # Calculate confidence based on extraction quality
        total_sents = len(list(doc.sents))
        classified = len(claims) + len(evidence)
        confidence = min(classified / total_sents if total_sents > 0 else 0.0, 1.0)
        
        # Boost confidence if we found good distribution
        if len(claims) > 0 and len(evidence) > 0:
            confidence = min(confidence + 0.2, 1.0)
        
        log_info(f"Advanced extraction: {len(claims)} claims, {len(evidence)} evidence, confidence={confidence:.2f}")
        
        return {
            "claims": claims,
            "evidence": evidence,
            "confidence": round(confidence, 2)
        }
    
    except Exception as e:
        log_error(f"Advanced extraction failed: {e}. Using fallback.")
        return extract_claims_and_evidence_fallback(text)


def extract_claims_and_evidence_fallback(text: str) -> Dict[str, object]:
    """Fallback keyword-based extraction (original implementation)."""
    if not text or not isinstance(text, str):
        return {"claims": [], "evidence": [], "confidence": 0.0}

    sentences = [s.strip() for s in text.split(".") if s.strip()]
    claim_keywords = ["is", "are", "will", "can", "should", "must"]
    claims: List[str] = []
    evidence: List[str] = []

    for s in sentences:
        if any(f" {kw} " in s.lower() for kw in claim_keywords):
            claims.append(s)
        else:
            evidence.append(s)

    total = len(sentences)
    classified = len(claims) + len(evidence)
    confidence = classified / total if total > 0 else 0.0

    return {"claims": claims, "evidence": evidence, "confidence": round(confidence, 2)}


def extract_claims_and_evidence(text: str) -> Dict[str, object]:
    """
    Extract claims and evidence from text using advanced NLP.
    Automatically falls back to keyword-based if needed.
    """
    return extract_claims_and_evidence_advanced(text)