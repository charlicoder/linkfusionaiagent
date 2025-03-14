from langgraph_sdk import get_sync_client, get_client
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn
import os
import uuid

load_dotenv()

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    token: str
    user_id: str
    user_name: str
    thread_id: str


# URL = os.getenv("CHAT_API_URL")
# print("=========URL========")
# print(URL)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://dev.ccsfusion.com",
    "https://app.linkfusions.com",
    "https://aiagent.linkfusions.com",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # Allow specific frontend URLs
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

config = {"configurable": {"thread_id": "1", "user_id": "1"}}

client = get_client(url="http://localhost:8123")


async def get_assistant(config: dict):
    assistant = await client.assistants.create(
        graph_id="agent",
        config=config,
        metadata={"number": 1},
        assistant_id=str(uuid.uuid4()),
        if_exists="do_nothing",
        name="my_name",
    )
    return assistant


@app.get("/hello")
def hello():
    return {"hello": "world"}


@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message
    token = request.token
    thread_id = request.thread_id
    user_id = request.user_id
    user_name = request.user_name
    config = {
        "configurable": {
            "token": token,
            "thread_id": thread_id,
            "user_id": user_id,
            "user_name": user_name,
        }
    }

    assistant = await get_assistant(config)

    runs = client.runs.stream(
        None,
        assistant_id=assistant["assistant_id"],
        input={"messages": [{"role": "user", "content": user_message}]},
        config=config,
        stream_mode="values",
    )

    final_response = None

    async for chunk in runs:  # Iterate asynchronously
        final_response = chunk  # Store the last response

    if final_response is None:
        raise HTTPException(
            status_code=500, detail="No response received from the assistant."
        )

    data = final_response.data["messages"][-1]
    return {"message": data["content"]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
