from langchain_core.tools import tool


@tool
def get_total_contacts_in_my_campaign():
    """
    It will returns the total number of contacts in campaign
    """

    return {
        "response": "This feature on development...! You will get total number of contacts very soon"
    }


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
]
