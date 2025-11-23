
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
# ---------------------------------------------------------

from workflow.orchestrator import Orchestrator

from fastapi import FastAPI
from pydantic import BaseModel
from workflow.orchestrator import Orchestrator
from db.database import save_history

app = FastAPI(title="Agentic Research Assistant API")

orchestrator = Orchestrator()

class QueryInput(BaseModel):
    query: str

@app.post("/query")
def run_query(data: QueryInput):
    response = orchestrator.run(data.query)
    save_history(data.query, response)
    return {"response": response}
