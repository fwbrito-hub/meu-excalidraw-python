from agno.agent import Agent
from agno.models.google import Gemini
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração do Agente Especialista
agente_excalidraw = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    description="Você é um Consultor Estratégico Sênior.",
    instructions=[
        "Sua missão é analisar diagramas em formato JSON gerados pelo Excalidraw.",
        "Esses diagramas podem representar arquiteturas de software, fluxogramas de processos organizacionais ou mapeamento de procedimentos operacionais.",
        "Seu foco de análise deve ser:",
        "1. Descrever o fluxo principal do desenho de forma clara e objetiva.",
        "2. Identificar possíveis falhas lógicas, gargalos, 'becos sem saída' ou falhas de segurança na estrutura apresentada.",
        "3. Sugerir melhorias práticas para otimizar o fluxo ou enriquecer o sistema.",
        "Seja direto, evite jargões desnecessários e responda sempre em Markdown bem estruturado em Português do Brasil."
    ],
    markdown=True
)

def analisar_diagrama(elementos: list):
    # Criamos o prompt técnico para a IA
    prompt = f"Analise este diagrama composto pelos seguintes elementos JSON: {str(elementos)}"
    
    # O Agente processa a mensagem
    resposta = agente_excalidraw.run(prompt)
    return resposta.content
