from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn
import uuid
from contextlib import asynccontextmanager
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

from pydantic import BaseModel
from code.agent import graph


class ChatRequest(BaseModel):
    message: str
    token: str
    user_id: str
    user_name: str
    thread_id: str
    env: str


origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://dev.ccsfusion.com",
    "https://app.linkfusions.com",
]


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Lifespan event handler for app startup and shutdown."""
#     global assistant
#     config = {
#         "configurable": {
#             "thread_id": "1",
#             "user_id": "1",
#             "user_name": "default_user",
#             "env": "production",
#             "token": "default_token",
#         }
#     }

#     print("Initializing assistant...")
#     assistant = await client.assistants.create(
#         graph_id="agent",
#         config=config,
#         metadata={"number": 1},
#         assistant_id=str(uuid.uuid4()),
#         if_exists="do_nothing",
#         name="my_name",
#     )
#     print("Assistant initialized successfully!")
#     print(f"{'*' * 20}")
#     print(assistant)

#     yield  # Application runs here

#     # Cleanup (if needed) when shutting down
#     print("Shutting down application...")


# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def hello():
    return {"hello": "world"}


@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat requests using the same assistant."""
    user_message = request.message
    config = {
        "configurable": {
            "token": request.token,
            "thread_id": request.thread_id,
            "user_id": request.user_id,
            "user_name": request.user_name,
            "env": request.env,
        }
    }
    input_message = HumanMessage(content=user_message)
    inputs = {"messages": [input_message]}

    response = graph.invoke(inputs, config)
    # print(response)
    data = response["messages"][-1]
    # print(data)
    return {"message": data.content}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
