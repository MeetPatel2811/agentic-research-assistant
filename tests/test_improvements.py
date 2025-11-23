import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from workflow.orchestrator import Orchestrator
from utils.logger import log_info

def test_error_handling():
    """Test that system handles errors gracefully."""
    log_info("=== Testing Error Handling ===")
    orchestrator = Orchestrator()
    
    # Test empty query
    result = orchestrator.run("")
    assert "empty" in result.lower()
    log_info("✅ Empty query handled correctly")
    
    # Test normal query
    result = orchestrator.run("What is agentic AI?")
    assert len(result) > 100
    log_info("✅ Normal query works")

def test_nlp_extraction():
    """Test advanced NLP claim extraction."""
    log_info("=== Testing NLP Extraction ===")
    from tools.custom.claim_evidence_extractor import extract_claims_and_evidence
    
    text = "AI systems are becoming more sophisticated. Research shows that 80% of companies use AI. This will continue to grow."
    result = extract_claims_and_evidence(text)
    
    assert len(result["claims"]) > 0
    assert "confidence" in result
    log_info(f"✅ NLP extraction works: {len(result['claims'])} claims found")

def test_web_search():
    """Test real web search."""
    log_info("=== Testing Web Search ===")
    from tools.built_in.web_search_tool import web_search
    
    results = web_search("agentic AI", top_k=3)
    assert len(results) > 0
    assert "title" in results[0]
    log_info(f"✅ Web search works: {len(results)} results found")

def test_database_recovery():
    """Test database corruption handling."""
    log_info("=== Testing Database Recovery ===")
    from db.database import verify_database_integrity, backup_database
    
    backup_database()
    is_ok = verify_database_integrity()
    assert is_ok
    log_info("✅ Database integrity verified")

if __name__ == "__main__":
    log_info("Starting comprehensive tests...")
    test_error_handling()
    test_nlp_extraction()
    test_web_search()
    test_database_recovery()
    log_info("=== ALL TESTS PASSED ===")