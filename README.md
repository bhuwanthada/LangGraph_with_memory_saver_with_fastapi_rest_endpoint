# LangGraph Agents with Memory + FastAPI REST Endpoint

This project demonstrates how to build a **LangGraph-based agentic workflow** with **interrupt handling** and **per-user memory**, exposed via a **FastAPI REST API**.

The solution uses a graph of simple agents (`agent_one`, `agent_two`, `agent_three`) where execution is **interrupted after `agent_two`**. Using LangGraph's checkpointing (`MemorySaver`), the system can **resume from the exact point of interruption** when the same user invokes the endpoint again.

---

## 🚀 Tech Stack

- **[LangGraph](https://python.langchain.com/docs/langgraph/)** – for agent orchestration and state management  
- **LangChain Tools** – to wrap Python functions as callable tools inside agents  
- **FastAPI** – lightweight web framework for building REST endpoints  
- **Pydantic** – request/response validation  
- **Uvicorn** – ASGI server to run the FastAPI app  
- **Python 3.10+** – recommended version  

---

## ⚙️ Project Features

- Multiple agents (`agent_one`, `agent_two`, `agent_three`) wired in a **LangGraph state machine**.  
- **Interrupt after `agent_two`** to simulate partial execution.  
- **Per-user memory management** via `MemorySaver`, isolated by `thread_id`.  
- **REST API endpoint** `/run-agents`:
  - Accepts `{ "message": "...", "user_id": "..." }`  
  - If the user is new → starts from scratch  
  - If memory exists and was interrupted → resumes from the point of interruption  
  - Otherwise → continues with updated state  

---

## 📂 Project Structure
.
├── main.py # FastAPI service + LangGraph compilation
├── requirements.txt
└── README.md
Clone the repository.
# clone repo
git clone https://github.com/your-username/langgraph-rest-agents.git
cd langgraph-rest-agents

# Create venv
python -m venv venv

# Activate venv
venv\Scripts\activate

# install requirements
pip install -r requirements.txt

# run Fastapi service
uvicorn main:api --reload

# API Usage
endpoint: POST /run-agents
request_body: 
```{
  "message": "Bhuwan",
  "user_id": "1"
}```

response:
```{
  "user_id": "Bhuwan",
  "current_message": "Hello, Bhuwan from agent-2",
  "message_history": [
    "start: 1",
    "agent_1: Hello, Bhuwan from agent-1",
    "agent_2: Hello, Bhuwan from agent-2"
  ]
}```


Run the same endpoint again.
response:
```{
  "user_id": "Bhuwan",
  "current_message": "Hello, Bhuwan from agent-3",
  "message_history": [
    "start: 1",
    "agent_1: Hello, Bhuwan from agent-1",
    "agent_2: Hello, Bhuwan from agent-2",
    "agent_3: Hello, Bhuwan from agent-3"
  ]
}```

Key Takeaways

Each user_id has its own thread of memory.

The workflow stops at interruptions and can resume automatically from where it left off.

FastAPI provides a clean REST interface to run and resume agent workflows.

Workflow Overview
sequenceDiagram
    participant U as User
    participant API as FastAPI (/run-agents)
    participant LG as LangGraph
    participant M as MemorySaver

    U->>API: POST /run-agents {message, user_id}
    API->>M: Check memory for user_id
    alt No memory
        API->>LG: Start new workflow
        LG->>M: Save state after agent_two (interrupt)
    else Memory exists with interrupt
        API->>LG: Resume from interrupt point
        LG->>M: Save resumed state
    end
    LG->>API: Return updated state
    API->>U: Response JSON