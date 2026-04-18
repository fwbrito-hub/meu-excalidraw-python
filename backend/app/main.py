from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
from typing import List, Any
import uuid
import time
from sqlalchemy.orm import Session
from app.database import SessionLocal, criar_tabelas, Projeto

# 1. Inicializando a aplicação
app = FastAPI(title="API v2 - AGORA COM IA")

# 2. Evento de Inicialização (Lugar mais seguro para o banco)
@app.on_event("startup")
def startup_event():
    print("Iniciando motor de banco de dados...")
    criar_tabelas()
    print("Banco de dados pronto para operacoes!")

# 3. Middleware para ver o que está acontecendo (Log de combate)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Rota acessada: {request.url.path} | Tempo: {process_time:.4f}s")
    return response

# 4. Dependência para o Banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProjetoExcalidraw(BaseModel):
    nome_projeto: str
    elementos_json: List[Any]

@app.get("/")
def status_da_base():
    return {"status": "Operacional", "servidor": "Ligado", "banco": "SQLite Ativo"}

@app.post("/api/projetos/salvar")
async def salvar_projeto(projeto: ProjetoExcalidraw, db: Session = Depends(get_db)):
    novo_projeto = Projeto(
        id=str(uuid.uuid4()),
        nome_projeto=projeto.nome_projeto,
        elementos_json=projeto.elementos_json
    )
    db.add(novo_projeto)
    db.commit()
    db.refresh(novo_projeto)
    return {"status": "Sucesso", "id": novo_projeto.id}

@app.get("/api/projetos/{id}")
def carregar_projeto(id: str, db: Session = Depends(get_db)):
    projeto = db.query(Projeto).filter(Projeto.id == id).first()
    return projeto if projeto else {"erro": "Não encontrado"}

# 8. Rota de Inteligência Artificial (Análise do Diagrama)
from app.agente.bot import analisar_diagrama

@app.post("/api/agente/analisar")
async def analisar_desenho(projeto: ProjetoExcalidraw):
    print(f"Acionando Inteligencia Artificial para: {projeto.nome_projeto}")
    try:
        analise = analisar_diagrama(projeto.elementos_json)
        return {"analise": analise}
    except Exception as e:
        return {"erro": f"Falha na comunicação com a IA: {str(e)}"}

