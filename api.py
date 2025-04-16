from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from dotenv import load_dotenv
import uvicorn
import uuid
import requests
from contextlib import asynccontextmanager
from langchain_core.messages import HumanMessage, SystemMessage
from code.aiagent.models import llm, llm_campaign
from code.utils import read_xlsx_file
import logging
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

logging.basicConfig(
    filename="logs.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)
logger = logging.getLogger(__name__)

from pydantic import BaseModel

# from code.agent import graph
from human import graph


class ChatRequest(BaseModel):
    message: str = (Form(...),)
    token: str = (Form(...),)
    thread_id: str = (Form(...),)
    user_id: str = (Form(...),)
    user_name: str = (Form(...),)
    env: str = (Form(...),)
    file: UploadFile = File(None)


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
async def chat_endpoint(
    message: str = Form(...),
    token: str = Form(...),
    thread_id: str = Form(...),
    user_id: str = Form(...),
    user_name: str = Form(...),
    env: str = Form(...),
    file: UploadFile = File(None),
):
    """Handle chat requests using the same assistant."""

    user_message = message
    config = {
        "configurable": {
            "token": token,
            "thread_id": thread_id,
            "user_id": user_id,
            "user_name": user_name,
            "env": env,
        }
    }
    import pdb

    if not user_message:
        return {"message": "Please explain what to do with your file"}

    if file:
        if not file.filename.endswith(".xlsx"):
            return {"message": "Only .xlsx files are supported."}

        contents = await file.read()
        print(f"Received file: {file.filename} with size {len(contents)} bytes")

        contacts_list = await read_xlsx_file(contents)
        contacts = contacts_list["data"]

        user_message += f" contacts {contacts}"

        messages = [
            SystemMessage(
                content="read the user message and try to get campaign name and action. "
                "action value upload_contact or import_contact. also return valid contacts in json format"
            ),
            HumanMessage(content=user_message),
        ]
        llmoutput = llm_campaign.invoke(messages)

        campaign_name = llmoutput.get("campaign_name")
        contacts_in_json = llmoutput.get("contacts")

        if campaign_name:
            user_message = f"Upload contacts to campaign {campaign_name}"
        else:
            return {
                "message": "No campaign name provided. Please try again with a campaign name."
            }

        req_url = f"{BASE_URL}/api/contacts/upload-contacts/"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        body = {"campaign_name": campaign_name, "contacts": contacts_in_json}
        try:
            response = requests.post(req_url, headers=headers, json=body)
            # response.raise_for_status()
            json_response = response.json()

            message_text = (
                f"Write a user friendly short message for the response: "
                f"{json_response['new_contacts_count']} new contacts added and "
                f"{json_response['updated_contacts_count']} updated"
            )
            # response = llm.invoke([HumanMessage(content=message_text)], config=config)
            response = llm.invoke(message_text, config=config)
            return {"message": response.content}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}", exc_info=True)
            return {"message": str(e)}

    input_message = HumanMessage(content=user_message)
    inputs = {"messages": [input_message]}
    print(f"config: {config}")
    response = graph.invoke(inputs, config)
    data = response["messages"][-1]
    return {"message": data.content}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
