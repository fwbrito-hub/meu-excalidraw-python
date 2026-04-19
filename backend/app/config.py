from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # 1. Configurações da API
    APP_NAME: str = "Excalidraw Python SaaS"
    DEBUG: bool = False

    # 2. IA / Agno (Puxado do .env)
    AGNO_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None # Caso use Gemini diretamente

    # 3. Banco de Dados
    DATABASE_URL: str = "sqlite:///./projeto.db"
    GEMINI_API_KEY: str = ""
    
    # Segurança JWT
    SECRET_KEY: str = "sua_chave_secreta_super_segura"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GOOGLE_API_KEY: str = ""

    # 4. Configuração do arquivo env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instância global para ser usada na aplicação
settings = Settings()
