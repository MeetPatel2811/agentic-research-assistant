# ---------------------------------------------------------
# run_tests.py
# This script runs automated test cases against the agentic
# research system. It prints metrics such as keyword coverage
# and response length for evaluation.
#
# It ALSO fixes Python module paths so imports work no matter
# where the script is executed.
# ---------------------------------------------------------

import sys
import os
import json
from typing import List, Dict, Any

# ---------------------------------------------------------
# FIX PYTHON PATHS
# Ensures Python can import from "src/" and "tests/" folders.
# ---------------------------------------------------------

# Directory: agentic_system/tests/run_tests.py
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory: agentic_system/
PROJECT_ROOT = os.path.dirname(TESTS_DIR)

# Directory: agentic_system/src/
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

# Add them to Python module search path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Debugging (optional):
# print("PYTHONPATH:", sys.path)

# ---------------------------------------------------------
# Now imports will work properly
# ---------------------------------------------------------
from workflow.orchestrator import Orchestrator
from tests.metrics import keyword_coverage, response_length_tokens


# ---------------------------------------------------------
# Helper: Load test cases from JSON file
# ---------------------------------------------------------
def load_test_cases(path: str) -> List[Dict[str, Any]]:
    """Loads test cases from test_cases.json."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------
# Main test runner
# ---------------------------------------------------------
def main() -> None:
    print("\n==================== RUNNING TESTS ====================\n")

    test_path = os.path.join(TESTS_DIR, "test_cases.json")
    cases = load_test_cases(test_path)

    orchestrator = Orchestrator()

    for case in cases:
        query = case["query"]
        expected_keywords = case.get("expected_keywords", [])

        print(f"--- Test Case: {case['id']} ---")
        print(f"Query: {query}")

        # Run system
        response = orchestrator.run(query)

        # Metrics
        cov = keyword_coverage(response, expected_keywords)
        length = response_length_tokens(response)

        print(f"Keyword Coverage: {cov}")
        print(f"Response Length: {length} tokens")
        print("Response Preview:")
        snippet = response[:400] + ("..." if len(response) > 400 else "")
        print(snippet)
        print("\n")

    print("==================== TESTS COMPLETE ====================\n")


# ---------------------------------------------------------
# Standard entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
