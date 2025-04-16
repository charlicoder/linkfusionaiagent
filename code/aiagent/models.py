from code.aiagent.tools import all_tools
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from code.aiagent.state import Router, CampaignNameOutput

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
llm_with_tools = llm.bind_tools(all_tools)
router_model = llm.with_structured_output(Router)
llm_campaign = llm.with_structured_output(CampaignNameOutput)
