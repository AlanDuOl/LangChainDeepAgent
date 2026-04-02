from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from tools.search import internet_search

# System prompt to steer the agent to be an expert researcher
research_instructions = """
You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

model = init_chat_model(
    model="ollama:qwen3.5:cloud",
    tools=[internet_search],
    system_prompt=research_instructions
)
agent = create_deep_agent(model=model)