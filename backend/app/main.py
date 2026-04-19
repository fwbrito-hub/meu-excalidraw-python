from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import List, Any, Optional
import time
from datetime import timedelta
from sqlalchemy.orm import Session

from app.database import get_db, Projeto, User
from app.config import settings
from app.auth import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_user
)

# 1. Inicializando a aplicação
app = FastAPI(title=settings.APP_NAME)

@app.on_event("startup")
def startup_event():
    # Garantir que o usuário Admin existe para o Modo Dev
    from app.database import SessionLocal, User
    from app.auth import get_password_hash
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "Admin").first()
        if not admin:
            new_admin = User(
                username="Admin",
                email="admin@excalisaas.com",
                hashed_password=get_password_hash("admin123")
            )
            db.add(new_admin)
            db.commit()
            print("--- MODO DEV: Usuário Admin criado com sucesso ---")
    finally:
        db.close()

# 2. Configurando CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos Pydantic ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProjetoExcalidraw(BaseModel):
    id: Optional[int] = None
    nome_projeto: str
    elementos_json: List[Any]

class RenameProjeto(BaseModel):
    nome_projeto: str

# --- Endpoints de Autenticação ---

@app.post("/api/auth/register", response_model=None)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuário criado com sucesso"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoints de Projetos (Protegidos) ---

@app.get("/")
def status_da_base():
    tipo_banco = "PostgreSQL Ativo" if "postgres" in settings.DATABASE_URL else "SQLite Ativo"
    return {"status": "Operacional", "servidor": "Ligado", "banco": tipo_banco, "auth": "JWT Habilitado"}

@app.get("/api/projetos", response_model=None)
def listar_projetos(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Projeto).filter(Projeto.owner_id == current_user.id).all()

@app.post("/api/projetos/salvar")
async def salvar_projeto(
    projeto: ProjetoExcalidraw, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if projeto.id:
        existing = db.query(Projeto).filter(Projeto.id == projeto.id, Projeto.owner_id == current_user.id).first()
        if not existing:
            raise HTTPException(status_code=404, detail="Projeto não encontrado para atualizar")
        existing.nome_projeto = projeto.nome_projeto
        existing.elementos_json = projeto.elementos_json
        db.commit()
        return {"status": "Atualizado", "id": existing.id}
    else:
        novo_projeto = Projeto(
            nome_projeto=projeto.nome_projeto,
            elementos_json=projeto.elementos_json,
            owner_id=current_user.id
        )
        db.add(novo_projeto)
        db.commit()
        db.refresh(novo_projeto)
        return {"status": "Criado", "id": novo_projeto.id}

@app.delete("/api/projetos/{id}")
def deletar_projeto(
    id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projeto = db.query(Projeto).filter(Projeto.id == id, Projeto.owner_id == current_user.id).first()
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
    db.delete(projeto)
    db.commit()
    return {"status": "Deletado"}

@app.put("/api/projetos/{id}/renomear")
def renomear_projeto(
    id: int,
    rename_data: RenameProjeto,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projeto = db.query(Projeto).filter(Projeto.id == id, Projeto.owner_id == current_user.id).first()
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
    
    projeto.nome_projeto = rename_data.nome_projeto
    db.commit()
    return {"status": "Renomeado"}

@app.get("/api/projetos/{id}")
def carregar_projeto(
    id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projeto = db.query(Projeto).filter(Projeto.id == id, Projeto.owner_id == current_user.id).first()
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
    return projeto

# --- IA ---
from app.agente.bot import analisar_diagrama

@app.post("/api/agente/analisar")
async def analisar_desenho(projeto: ProjetoExcalidraw, current_user: User = Depends(get_current_user)):
    try:
        analise = analisar_diagrama(projeto.elementos_json)
        return {"analise": analise}
    except Exception as e:
        return {"erro": str(e)}
