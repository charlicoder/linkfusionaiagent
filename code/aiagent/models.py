from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from code.aiagent.state import Router

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
router_model = llm.with_structured_output(Router)
