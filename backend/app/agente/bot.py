from agno.agent import Agent
from agno.models.google import Gemini
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração do Agente Especialista
agente_excalidraw = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    description="Você é um especialista em arquitetura de sistemas e diagramas.",
    instructions=[
        "Você receberá um JSON contendo elementos de um desenho do Excalidraw.",
        "Sua tarefa é analisar as formas, textos e conexões.",
        "Explique o que o diagrama representa e dê sugestões de melhoria.",
        "Responda sempre em Português do Brasil, de forma clara e técnica."
    ],
    markdown=True
)

def analisar_diagrama(elementos: list):
    # Criamos o prompt técnico para a IA
    prompt = f"Analise este diagrama composto pelos seguintes elementos JSON: {str(elementos)}"
    
    # O Agente processa a mensagem
    resposta = agente_excalidraw.run(prompt)
    return resposta.content
