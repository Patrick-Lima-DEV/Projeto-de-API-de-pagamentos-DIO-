from fastapi import FastAPI
from app.routes.pagamento import pagamento_router
from app.routes.auth import auth_router
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()

# Criar diretório de logs se não existir
os.makedirs('logs', exist_ok=True)

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Pagamentos com Azure",
    description="API segura para simulação de pagamentos com autenticação JWT e rate limiting",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    logger.warning(f"Rate limit excedido para {request.client.host}")
    return JSONResponse(
        status_code=429,
        content={"detail": "Muitas requisições. Tente novamente mais tarde."},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("API iniciada com sucesso")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API finalizada")

@app.get("/", tags=["health"])
async def root():
    logger.info("Health check realizado")
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(pagamento_router, prefix="/pagamentos", tags=["pagamentos"])
