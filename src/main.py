# This is the entry point for the agentic system.
# It creates an Orchestrator and lets the user type queries from the console.

import os
import sys

# This block ensures that the current src directory is on sys.path
# so that imports of "agents", "controller", etc. work when running main.py directly.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from workflow.orchestrator import Orchestrator  # type: ignore  # noqa: E402
from utils.logger import log_info  # type: ignore  # noqa: E402


def main() -> None:
    # This function runs a simple CLI loop for testing the agentic system.
    orchestrator = Orchestrator()
    log_info("Agentic Research Assistant is ready.")

    while True:
        # This loop reads user queries until 'quit' is entered.
        query = input("\nEnter your research question (or type 'quit' to exit): ").strip()
        if query.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        # This triggers the entire multi-agent pipeline for the given query.
        response = orchestrator.run(query)
        print("\n======== AGENTIC SYSTEM RESPONSE ========\n")
        print(response)
        print("\n=========================================")


if __name__ == "__main__":
    main()
