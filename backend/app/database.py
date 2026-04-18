from sqlalchemy import create_engine, Column, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# 1. URL de Conexão (12-Factor: Config)
# No futuro, essa URL virá do arquivo .env
SQLALCHEMY_DATABASE_URL = "sqlite:///./projeto.db"

# 2. Criando o motor (Engine) do Banco
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Sessão de Banco de Dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base para os nossos Modelos
Base = declarative_base()

# 5. Modelo da Tabela Projetos (Conforme nosso SDD!)
class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(String, primary_key=True, index=True)
    nome_projeto = Column(String, index=True)
    elementos_json = Column(JSON)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# 6. Função para criar as tabelas
def criar_tabelas():
    Base.metadata.create_all(bind=engine)
