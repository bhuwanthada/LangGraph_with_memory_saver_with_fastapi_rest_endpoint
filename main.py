from fastapi import FastAPI
from agents import compile_graph
from pydantic import BaseModel

app = FastAPI()

graph_app = None
graph_memory = None


class MessageInput(BaseModel):
    message: str
    user_id: str


@app.on_event("startup")
async def startup_event():
    global graph_app, graph_memory
    graph_memory, graph_app = compile_graph()
    print("Graph compiled and ready to use.")


@app.post("/run-agents")
async def run_agents(input_data: MessageInput):
    global graph_app, graph_memory
    config = {"configurable": {"thread_id": input_data.user_id}}
    if not graph_app:
        return {"error": "Graph not initialized"}
        # Check if user already has memory
    stored_state = graph_memory.get(config)
    if stored_state and "channel_values" in stored_state:
        # Continue from existing memory
        print(f"Resuming for user {input_data.user_id}")
        result = graph_app.invoke(None, config)
        print(f"result from memory: {result}")

    else:
        # Start fresh
        print(f"Starting new session for user {input_data.user_id}")
        init_state = {
            "current_message": input_data.message,
            "message_history": [f"start: {input_data.message}"],
            "user_id": input_data.user_id,
        }

        # Run graph with memory + config
        result = graph_app.invoke(init_state, config=config)
        print(f"result from fresh: {result}")
    return result