# Excalidraw Customizado com Python e Agno AI

Projeto desenvolvido seguindo os princípios de **Spec-Driven Development (SDD)** e **12-Factor App**.

## Estrutura do Projeto
- `docs/`: Documentação técnica e SDD.
- `backend/`: API FastAPI e integração com Agno AI.
- `frontend/`: Interface React com Excalidraw.

## 🎓 Trilha de Aprendizado: SaaS Elite

Este repositório foi projetado como um **Curso Interativo**. Siga os passos abaixo para aprender a construir este SaaS:

1. **Setup Inicial:** Rode `python course/bootstrap_course.py` no terminal.
2. **Lição 01:** [Setup e Arquitetura](course/01_setup_e_arquitetura.ipynb) - Entenda o coração do sistema.
3. **Lição 02:** [DB e Migrations](course/02_banco_de_dados_e_migrations.ipynb) - Evolua seu banco sem perder dados.
4. **Lição 03:** [Segurança SaaS (JWT)](course/03_seguranca_e_auth_jwt.ipynb) - Proteja os segredos dos seus usuários.
5. **Bônus:** [Deploy em Produção](course/04_deploy_producao_bonus.ipynb) - Coloque seu produto no ar.

*Gabaritos disponíveis na pasta `/course/solutions`.*

---

## Como rodar o Backend
1. Acesse a pasta `backend`
2. Crie um ambiente virtual: `python -m venv venv`
3. Instale as dependências: `pip install -r requirements.txt`
4. Configure o arquivo `.env` baseado no `.env.example`
5. Execute: `uvicorn app.main:app --reload`
