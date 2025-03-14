from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
import requests
from dotenv import load_dotenv
import logging
import os

load_dotenv()

# Configure logging
logging.basicConfig(
    filename="logs.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL")


print(f"{'*'*10} {BASE_URL}")


@tool
def get_total_contacts_in_my_campaign():
    """
    It will returns the total number of contacts in campaign
    """

    return {
        "response": "This feature on development...! You will get total number of contacts very soon"
    }


@tool
def get_campaign_list(config: RunnableConfig):
    """
    Returns list of campaigns for the requested user
    """

    user_id = config.get("configurable", {}).get("user_id")
    token = config.get("configurable", {}).get("token")
    req_url = f"{BASE_URL}/api/marketing/campaigns/"

    headers = {"Authorization": f"Bearer {token}"}

    # logger.debug(f"Fetching campaigns for user_id: {user_id}")
    # logger.debug(f"Request URL: {req_url}")
    # logger.debug(f"Request Headers: {headers}")

    try:
        response = requests.get(req_url, headers=headers)
        response.raise_for_status()
        json_response = response.json()

        # logger.debug(f"Response Status: {response.status_code}")
        # logger.debug(f"Response JSON: {json_response}")

        return {"response": json_response}  # Ensure the response is returned as JSON
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        return {"error": str(e)}


@tool
def create_campaign(name: str, company: str, config: RunnableConfig):
    """
    Create a marketing campaign.

    Args:
        name (str): Name of the campaign.
        company (str): Name of the company.
        config (RunnableConfig): Configuration object with user authentication details.

    Returns:
        dict: Response JSON or error message.
    """
    print(f"Creating campaign: {name} for company: {company}")

    user_id = config.get("configurable", {}).get("user_id")
    token = config.get("configurable", {}).get("token")

    if not token:
        logger.error("Authorization token is missing in config.")
        return {"error": "Missing authentication token."}

    req_url = f"{BASE_URL}/api/marketing/campaigns/"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    body = {"company": company, "name": name}

    try:
        response = requests.post(req_url, headers=headers, json=body, timeout=10)
        response.raise_for_status()

        json_response = response.json()
        logger.info(f"Campaign created successfully: {json_response}")
        return {"response": json_response}  # Ensure the response is returned as JSON

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        return {"error": str(e)}


@tool
def get_campaign_status():
    """
    Agent will campaign status defined by LinkFusion
    """

    return {
        "response": "This feature on development...! You will get campaign status very soon"
    }


@tool
def get_total_new_contacts_added():
    """
    Return total new contacts added to a campaign today.
    """
    return {
        "response": "This feature on development...! You will get total new contacts added to a campaign very soon"
    }


all_tools = [
    get_total_contacts_in_my_campaign,
    get_campaign_status,
    get_total_new_contacts_added,
    create_campaign,
    get_campaign_list,
]
