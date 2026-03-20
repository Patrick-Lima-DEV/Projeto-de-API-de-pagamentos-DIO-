from fastapi import APIRouter, Depends, Request
from app.models.pagamento import Pagamento
from app.controllers.pagamento_controller import listar_pagamentos, criar_pagamento, atualizar_pagamento, deletar_pagamento
from app.middlewares.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)

pagamento_router = APIRouter()

# GET - Listar pagamentos
@pagamento_router.get(
    "/",
    response_model=list,
    summary="Listar pagamentos",
    description="Retorna lista de todos os pagamentos"
)
@limiter.limit("30/minute")
async def get_pagamentos(request: Request):
    return await listar_pagamentos()

# POST - Criar pagamento
@pagamento_router.post(
    "/",
    response_model=dict,
    summary="Criar pagamento",
    description="Cria um novo pagamento (requer autenticação)"
)
@limiter.limit("10/minute")
async def post_pagamento(request: Request, pagamento: Pagamento, user=Depends(get_current_user)):
    return await criar_pagamento(pagamento, user)

# PUT - Atualizar pagamento
@pagamento_router.put(
    "/{id}",
    response_model=dict,
    summary="Atualizar pagamento",
    description="Atualiza um pagamento existente (requer autenticação)"
)
@limiter.limit("10/minute")
async def put_pagamento(request: Request, id: int, pagamento: Pagamento, user=Depends(get_current_user)):
    return await atualizar_pagamento(id, pagamento, user)

# DELETE - Deletar pagamento
@pagamento_router.delete(
    "/{id}",
    summary="Deletar pagamento",
    description="Deleta um pagamento existente (requer autenticação)"
)
@limiter.limit("10/minute")
async def delete_pagamento(request: Request, id: int, user=Depends(get_current_user)):
    return await deletar_pagamento(id, user)
