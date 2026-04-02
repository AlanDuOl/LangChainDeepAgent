import os
from pathlib import Path
from ollama import Client
from langchain_core.tools import tool

# Definimos a "Sandbox" (Pasta Segura)
OUTPUT_DIR = Path("./searchs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # Cria a pasta se não existir

ollama_client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

    
def safe_write_file(filename: str, content: str):
    """
    Escreve conteúdo em um arquivo de texto de forma segura dentro da pasta permitida.
    Restrições: Apenas arquivos .txt ou .md são permitidos.
    """
    try:
        # 1. Remove qualquer tentativa de usar caminhos relativos (../)
        clean_name = Path(filename).name 
        
        # 2. Validação de Extensão
        if not clean_name.endswith('.md'):
            return "Erro: Apenas extensões .md são permitidas por segurança."

        # 3. Define o caminho final absoluto dentro da sandbox
        file_path = OUTPUT_DIR / clean_name
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"Arquivo '{clean_name}' criado com sucesso em {OUTPUT_DIR}."
    
    except Exception as e:
        return f"Falha na operação: {str(e)}"


@tool
def write_file(messages: list[dict]):
    """Cria um arquivo no sistema com o conteúdo fornecido."""
    # 1. Chamar o agente para criar o arquivo
    response = ollama_client.chat(
        messages=messages,
    )

    # 2. Verificamos se o modelo solicitou o uso da ferramenta (Tool Call)
    if response['message'].get('tool_calls'):
        for tool in response['message']['tool_calls']:
            if tool['function']['name'] == 'write_file':
                # Pegamos os argumentos que o modelo gerou (filename e content)
                args = tool['function']['arguments']
                
                print(f"--- Executando Tool: write_file para {args['filename']} ---")
                
                # Executamos a função real no Python
                return safe_write_file(**args)

        return f"tool write_file não encontrada. tool_calls: {response['message']['tool_calls']}"
    else:
        return f"tool_calls não encontrado na resposta: {response['message']}"


