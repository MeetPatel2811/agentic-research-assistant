# Agentic Research Assistant  
A full-stack multi-agent research system built with Python, FastAPI, Streamlit, and a custom multi-agent orchestration engine.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

---

# 🌟 Overview

**Agentic Research Assistant** is a fully functional multi-agent AI system designed for the *Building Agentic Systems* course.  
It demonstrates **agent orchestration**, **tool integration**, **memory management**, **feedback loops**, and **full-stack deployment**.

Unlike typical LLM chat apps, this system uses cooperating agents, each with specialized skills, guided by a central Controller Agent.

This project is designed to be:
- **Fully local (no API keys needed)**
- **Lightweight**
- **End-to-end functional**
- **Highly educational**
- **TA-impressive**

---

# ✨ Key Features

### 🤖 Multi-Agent Orchestration
- Controller Agent  
- Research Agent  
- Analysis Agent  
- Writer Agent  
- Clear communication protocol

### 🔍 Built-In Research Tools
- Web Search Tool  
- Summarization Tool  
- Markdown Formatter Tool  

### 🧠 Custom Tool
**Claim–Evidence Extractor**  
Extracts structured insights from research summaries.

### 💾 Advanced Memory System
- JSON memory store
- SQLite long-term history database
- Cross-agent context preservation

### 🎯 RL-Inspired Feedback Loop
- Automatic quality scoring
- Retry mechanism for low-quality outputs

### 💻 Professional Full-Stack Architecture
- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Storage:** SQLite  
- **Orchestration:** Python multi-agent pipeline  

---

# 🏗️ Architecture
flowchart TD

    %% FRONTEND LAYER
    U[User] --> UI[Streamlit Frontend<br/>frontend/app.py]

    %% API LAYER
    UI -->|POST /query| API[FastAPI Server<br/>api/main.py]

    %% ORCHESTRATION LAYER
    API --> ORCH[Orchestrator<br/>src/workflow/orchestrator.py]

    %% CONTROLLER
    ORCH --> CTRL[Controller Agent<br/>src/controller/controller.py]

    %% AGENTS
    CTRL --> RA[Research Agent<br/>src/agents/research_agent.py]
    CTRL --> AA[Analysis Agent<br/>src/agents/analysis_agent.py]
    CTRL --> WA[Writer Agent<br/>src/agents/writer_agent.py]

    %% TOOLS
    RA --> WS[Web Search Tool<br/>src/tools/built_in/web_search_tool.py]
    AA --> SM[Summarizer Tool<br/>src/tools/built_in/summarizer_tool.py]
    AA --> CE[Custom Claim–Evidence Extractor<br/>src/tools/custom/claim_evidence_extractor.py]
    WA --> FM[Formatter Tool<br/>src/tools/built_in/formatter_tool.py]

    %% MEMORY SYSTEM
    CTRL --> MEM[Memory Manager<br/>src/memory/memory_manager.py]
    MEM --> JSON[(memory_store.json)]
    API --> DB[(SQLite DB\nhistory.db)]

    %% RL FEEDBACK LOOP
    CTRL --> RL[Feedback Loop<br/>src/rl/feedback_loop.py]
    RL --> CTRL

    %% RETURN PATH
    ORCH --> API --> UI --> U


### 🧩 Agents
| Agent | Role |
|-------|------|
| **Controller** | Orchestrates workflow, handles retries |
| **Research Agent** | Retrieves domain-specific documents |
| **Analysis Agent** | Summarizes & extracts claims/evidence |
| **Writer Agent** | Produces clean markdown reports |

### ⚙️ Tools
- `web_search_tool.py`
- `summarizer_tool.py`
- `formatter_tool.py`
- `claim_evidence_extractor.py` (custom)

### 🧱 Technology Stack
- **Backend:** Python, FastAPI  
- **Frontend:** Streamlit  
- **Database:** SQLite  
- **Agents:** Custom Python framework  
- **Testing:** Python test suite

---

# 🚀 Quick Start

##  **1. Clone the repository**
```bash
git clone <your-repo-url>
cd agentic_system
```

##  **2. Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

##  **3. Install dependencies**
```bash
pip install -r requirements.txt
```

##  **4. Run the FastAPI backend**
```bash
uvicorn api.main:app --reload
```
Visit API docs at:  
👉 http://127.0.0.1:8000/docs

##  **5. Run the Streamlit frontend**
Open a new terminal tab:
```bash
source venv/bin/activate
cd frontend
streamlit run app.py
```
Access the UI at:  
👉 http://localhost:8501

---

# 📁 Project Structure

```
agentic_system/
├── api/
│   └── main.py
├── frontend/
│   ├── app.py
│   └── utils/api_client.py
├── db/
│   ├── database.py
│   └── history.db
├── src/
│   ├── agents/
│   ├── controller/
│   ├── tools/
│   ├── memory/
│   ├── rl/
│   ├── utils/
│   └── main.py
├── tests/
├── docs/
├── README.md
└── requirements.txt
```

---

# 🔧 Configuration

This project requires *no API keys* — all data is local.

### Optional Settings
Located in `db/database.py`  
- Database path  
- Table creation  

---

# 📊 API Endpoints

### **POST /query**
Run agentic research pipeline.

Example:

```json
{
  "query": "What are agentic AI systems?"
}
```

Response contains:
- Overview  
- Claims  
- Evidence  
- Sources  
- Formatting  
- Metadata  

---

# 🧪 Testing

Run all tests:

```bash
python3 tests/run_tests.py
```

Outputs:
- Keyword coverage  
- Response length  
- Pipeline validation  
- Preview of output  

---

# 💡 Sample Research Queries

- "What is agentic AI?"
- "How does multi-agent orchestration work?"
- "How is reinforcement learning used to improve agents?"
- "Advantages of specialized AI agents"

---

# 🔍 Core Components

### Custom Claim–Evidence Extractor
- Lightweight NLP logic  
- Generates structured insights  
- Adds analytical layers to summaries  

### Controller Logic
- Task routing  
- Error handling  
- Retry mechanism  
- Feedback integration  

### Full Stack Integration
- Streamlit → FastAPI → Orchestrator → SQLite → UI  

---


---

# 🎬 Demo

### What the demo shows:
- Full system execution
- Agent logs in terminal
- FastAPI endpoint working
- Streamlit UI with live results
- History retrieval from SQLite  
- Claims + evidence extraction

---

# 🛠️ Development

### Add new tools:
Place them in `src/tools/custom/`  
Update the analysis agent to integrate.

### Add new agents:
Add to `/src/agents`  
Update orchestrator routing.

### Extend UI:
Modify `/frontend/app.py`

---

# 🏆 Achievements

- Full working multi-agent system  
- End-to-end architecture  
- Real-time interaction  
- Clean UI and REST API  
- Structured analysis capabilities  
- TA-level production polish  

---


**Built with ❤️ as part of INFO 7375 – Building Agentic Systems**

