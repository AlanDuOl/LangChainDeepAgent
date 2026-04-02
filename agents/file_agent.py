from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from tools.file import write_file

# System prompt to steer the agent to be an expert file agent
create_file_instructions = """
You are a specialized File Writer. 
Your ONLY goal is to take the text provided and save it using the 'write_file' tool.

IMPORTANT: 
- Use the filename provided in the request.
- Do not try to 'check' if the file exists using other tools. 
- Just call 'write_file' and report the success message returned by the tool.
"""

model = init_chat_model(
    model="ollama:qwen3.5:cloud",
    tools=[write_file],
    system_prompt=create_file_instructions
)
agent = create_deep_agent(model=model)