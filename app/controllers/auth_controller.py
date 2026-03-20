from fastapi import HTTPException
from app.middlewares.auth import authenticate_user, create_access_token
from fastapi import Request
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class LoginRequest(BaseModel):
    username: str
    password: str

async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        client_host = request.client.host if request.client else "unknown"
        logger.warning(f"Tentativa de login com credenciais incompletas de {client_host}")
        raise HTTPException(status_code=400, detail="Username e password são obrigatórios")
    
    user = authenticate_user(username, password)
    if not user:
        client_host = request.client.host if request.client else "unknown"
        logger.warning(f"Falha de autenticação para usuario {username} de {client_host}")
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = create_access_token(user)
    logger.info(f"Usuario {username} autenticado com sucesso")
    return {"access_token": token, "token_type": "bearer"}
