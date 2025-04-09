from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
import requests
from dotenv import load_dotenv
import logging
import os
from datetime import datetime, timedelta
from typing import Optional

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


@tool
def get_total_contacts_in_my_campaign(
    campaign_name: str, folder_name: str, config: RunnableConfig
):
    """
    Returns the total number of contacts in campaign if name is provided else returns total contacts for the user

    Args:
        campaign_name (str): Name of the campaign to get contacts from
        folder_name (str): Name of a folder to filter contacts by
        config (RunnableConfig): Configuration object with user authentication details.

    Returns:
        dict: List of contacts

    """
    user_id = config.get("configurable", {}).get("user_id")
    token = config.get("configurable", {}).get("token")

    req_url = f"{BASE_URL}/api/contacts/contact-stats/"

    headers = {"Authorization": f"Bearer {token}"}

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
        dict: Response JSON or error message. Return link to new created campaign link if posibble with base url {BASE_URL}
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
def get_campaign_status(campaign_name: str, config: RunnableConfig):
    """
    Return status of all campaigns or a specific campaign if name is provided. Status contains following information:
        email count, contacts count

    Args:
        campaign_name (str): Campaign name
        config (RunnableConfig): Configuration object with user authentication details.

    Returns:
        dict: Status of all campaigns or a specific campaign in name is provided

    """

    user_id = config.get("configurable", {}).get("user_id")
    token = config.get("configurable", {}).get("token")

    req_url = f"{BASE_URL}/api/marketing/campaigns/stats/"

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


def get_total_new_contacts_added(
    date: Optional[str] = None,
    campaign_name: Optional[str] = None,
    config: RunnableConfig = None,
):
    """
    Return total new contacts added to a campaign. If no campaign name is provided, get the count for all campaigns.
    Generate date from the string.

    Args:
        date (Optional[str]): Date string in format '%d/%m/%Y'. If no date is given, use today's date.
        campaign_name (Optional[str]): Name of the campaign.
        config (Optional[RunnableConfig]): Configuration for execution.

    Returns:
        dict: Returns a list of contacts in a campaign or all campaigns added after the provided date or today.
    """

    if date is None:
        date = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        print(date)

    user_id = config.get("configurable", {}).get("user_id")
    token = config.get("configurable", {}).get("token")

    req_url = f"{BASE_URL}/api/contacts/new-contacts/"

    headers = {"Authorization": f"Bearer {token}"}

    params = {}
    if date:
        params["d"] = date
    if campaign_name:
        params["cname"] = campaign_name

    # logger.debug(f"Fetching campaigns for user_id: {user_id}")
    # logger.debug(f"Request URL: {req_url}")
    # logger.debug(f"Request Headers: {headers}")

    try:
        response = requests.get(req_url, headers=headers, params=params)
        response.raise_for_status()
        json_response = response.json()

        # logger.debug(f"Response Status: {response.status_code}")
        # logger.debug(f"Response JSON: {json_response}")

        return {"response": json_response}  # Ensure the response is returned as JSON
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        return {"error": str(e)}


@tool
def create_fusion_card(fusion_card_name: str, config: RunnableConfig):
    """
    Create a fusion card.

    Args:
        fusion_card_name (str): Name of the campaign.
        config (RunnableConfig): Configuration object with user authentication details.

    Returns:
        dict: Return response as message with link to new created fusion card link if posibble with base url {BASE_URL}

    Example:
        output: The fusion card named "alayna" has been created successfully. Here are the details:

                    Fusion Card ID: 76
                    Contact ID: 140490
                    Status: Success
                    Message: Form submitted successfully
                    URL: Fusion Card Update
                    If you need any further assistance, feel free to ask!
    """
    user_id = config.get("configurable", {}).get("user_id")
    token = config.get("configurable", {}).get("token")

    if not token:
        logger.error("Authorization token is missing in config.")
        return {"error": "Missing authentication token."}

    req_url = f"{BASE_URL}/api/marketing/create-fusion-card-api/"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    body = {"fusion_card_name": fusion_card_name}

    try:
        response = requests.post(
            req_url,
            headers=headers,
            json=body,
        )
        response.raise_for_status()
        json_response = response.json()

        return {"response": json_response}  # Ensure the response is returned as JSON
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        return {"error": str(e)}


@tool
def get_list_of_fusion_cards(config: RunnableConfig):
    """
    Return list of fusion cards
    """
    user_id = config.get("configurable", {}).get("user_id")
    token = config.get("configurable", {}).get("token")

    if not token:
        logger.error("Authorization token is missing in config.")
        return {"error": "Missing authentication token."}

    req_url = f"{BASE_URL}/api/contacts/fusion-card-list/"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        response = requests.get(req_url, headers=headers)
        response.raise_for_status()
        json_response = response.json()

        return {"response": json_response}  # Ensure the response is returned as JSON
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        return {"error": str(e)}


all_tools = [
    get_total_contacts_in_my_campaign,
    get_campaign_status,
    get_total_new_contacts_added,
    create_campaign,
    get_campaign_list,
    get_list_of_fusion_cards,
    create_fusion_card,
]
