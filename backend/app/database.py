from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
from app.config import settings

# 1. URL de Conexão
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 2. Criando o motor (Engine) do Banco
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

# 3. Sessão de Banco de Dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base para os nossos Modelos
Base = declarative_base()

# 5. Modelo de Usuário
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Relacionamento: Um usuário tem muitos projetos
    projetos = relationship("Projeto", back_populates="owner")

# 6. Modelo de Projeto (Vinculado a Usuário)
class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome_projeto = Column(String, index=True)
    elementos_json = Column(JSON)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # FK para o dono do projeto
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relacionamento de volta para o usuário
    owner = relationship("User", back_populates="projetos")

# 7. Criando as tabelas (caso não existam)
Base.metadata.create_all(bind=engine)

# 8. Dependência para injetar o DB e fechar após uso
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
