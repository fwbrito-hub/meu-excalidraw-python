# Excalidraw Customizado com Python e Agno AI

Projeto desenvolvido seguindo os princípios de **Spec-Driven Development (SDD)** e **12-Factor App**.

## Estrutura do Projeto
- `docs/`: Documentação técnica e SDD.
- `backend/`: API FastAPI e integração com Agno AI.
- `frontend/`: Interface React com Excalidraw.

## Como rodar o Backend
1. Acesse a pasta `backend`
2. Crie um ambiente virtual: `python -m venv venv`
3. Instale as dependências: `pip install -r requirements.txt`
4. Configure o arquivo `.env` baseado no `.env.example`
5. Execute: `uvicorn app.main:app --reload`
