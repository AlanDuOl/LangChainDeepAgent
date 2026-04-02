import os
from typing import Literal
from ollama import Client
from deepagents import create_deep_agent

ollama_client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return ollama_client.web_search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )