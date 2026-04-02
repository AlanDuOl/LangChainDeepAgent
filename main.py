import os
# from pathlib import Path
from agents.search_agent import agent as search_agent
from agents.file_agent import agent as file_agent
# from ollama import Client
# from tools.file import safe_write_file



# messages = []
print("inicio busca")
response = search_agent.invoke({"messages": [{"role": "user", "content": "What is langgraph?"}]})
print("fim busca")
# print(response["messages"][-1].content)
# print(response["messages"][-1].tool_calls)
# messages.append(response['messages'])

print("inicio criar arquivo")
response = file_agent.invoke({"messages": [{"role": "user", "content": f"Crie um arquivo chamado /searchs/internet_search.md com o texto: '{response["messages"][-1].content}'"}]})

print("fim criar arquivo")
print("--- Finalizando e Sincronizando Arquivos ---")

# O objeto 'response' contém a estrutura virtual 'files' que o agente criou
if "files" in response:
    for v_path, data in response["files"].items():
        # Converte o caminho virtual /searchs/file.txt em ./searchs/file.txt
        local_path = os.path.join(".", v_path.lstrip("/"))
        
        # Cria a pasta
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Salva o conteúdo (que vem como uma lista de linhas no seu log)
        conteudo_final = "\n".join(data["content"])
        
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(conteudo_final)
            
        print(f"✅ Arquivo sincronizado com sucesso: {local_path}")

