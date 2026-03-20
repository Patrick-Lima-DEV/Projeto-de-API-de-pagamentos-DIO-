from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET", "segredo_super_secreto")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

fake_user = {
    "username": "usuario_demo",
    "password": pwd_context.hash("senha123")
}

def authenticate_user(username, password):
    """Valida credenciais do usuário"""
    if username != fake_user["username"]:
        logger.debug(f"Tentativa de autenticação com usuario desconhecido: {username}")
        return False
    if not pwd_context.verify(password, fake_user["password"]):
        logger.debug(f"Senha incorreta para usuario: {username}")
        return False
    logger.debug(f"Usuario autenticado: {username}")
    return {"username": username}

def create_access_token(user):
    """Cria um token JWT para o usuário"""
    token = jwt.encode({"sub": user["username"]}, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"Token JWT criado para usuario: {user['username']}")
    return token

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Valida e retorna o usuário atual do token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            logger.warning("Token JWT inválido: sub não encontrado")
            raise HTTPException(status_code=401, detail="Token inválido")
        logger.debug(f"Usuario extraído do token: {username}")
        return {"username": username}
    except JWTError as e:
        logger.warning(f"Erro ao decodificar JWT: {str(e)}")
        raise HTTPException(status_code=401, detail="Token inválido")
