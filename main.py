import os
from dotenv import load_dotenv

from src.agent.agent import ReActAgent
from src.core.openai_provider import OpenAIProvider

load_dotenv()  # load variables from .env

provider = OpenAIProvider(
    model_name=os.getenv("DEFAULT_MODEL", "gpt-5.4-mini"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

tools = []  # add your tool definitions here
agent = ReActAgent(llm=provider, tools=tools)

print(agent.run("Hello"))
