from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app import database

# 1. Contexto para Hashing de Senhas (Argon2 - Mais seguro e estável em 3.13)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# 2. Esquema OAuth2 para extrair o token do Header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # --- MODO DESENVOLVEDOR (Auto-Login com token estático) ---
    # Este bloco é ativado pelo token 'dev-admin-token' OU quando DEBUG=True no .env
    is_dev_token = (token == "dev-admin-token")
    if is_dev_token or settings.DEBUG:
        if is_dev_token:
            user = db.query(database.User).filter(database.User.username == "Admin").first()
            if user:
                return user
            # Se o usuário Admin não foi criado ainda, cria agora
            new_admin = database.User(
                username="Admin",
                email="admin@excalisaas.com",
                hashed_password=get_password_hash("admin123")
            )
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            return new_admin
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(database.User).filter(database.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
