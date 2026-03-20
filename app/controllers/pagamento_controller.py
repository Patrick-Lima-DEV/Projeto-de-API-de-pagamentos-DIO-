from fastapi import Depends, HTTPException
from app.models.pagamento import Pagamento
from app.services.pagamento_service import pagamentos, add_pagamento, update_pagamento, delete_pagamento
from app.middlewares.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

async def listar_pagamentos():
    logger.info(f"Listando {len(pagamentos)} pagamentos")
    return pagamentos

async def criar_pagamento(pagamento: Pagamento, user=Depends(get_current_user)):
    try:
        resultado = add_pagamento(pagamento)
        logger.info(f"Usuario {user['username']} criou pagamento ID {resultado['id']}")
        return resultado
    except Exception as e:
        logger.error(f"Erro ao criar pagamento: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao criar pagamento")

async def atualizar_pagamento(id: int, pagamento: Pagamento, user=Depends(get_current_user)):
    if id <= 0:
        logger.warning(f"Tentativa de atualizar pagamento com ID inválido: {id}")
        raise HTTPException(status_code=400, detail="ID deve ser um inteiro positivo")
    
    try:
        resultado = update_pagamento(id, pagamento)
        if "erro" in resultado:
            logger.warning(f"Pagamento ID {id} não encontrado para atualização")
            raise HTTPException(status_code=404, detail=resultado["erro"])
        logger.info(f"Usuario {user['username']} atualizou pagamento ID {id}")
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar pagamento ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar pagamento")

async def deletar_pagamento(id: int, user=Depends(get_current_user)):
    if id <= 0:
        logger.warning(f"Tentativa de deletar pagamento com ID inválido: {id}")
        raise HTTPException(status_code=400, detail="ID deve ser um inteiro positivo")
    
    try:
        resultado = delete_pagamento(id)
        if "erro" in resultado:
            logger.warning(f"Pagamento ID {id} não encontrado para deleção")
            raise HTTPException(status_code=404, detail=resultado["erro"])
        logger.info(f"Usuario {user['username']} deletou pagamento ID {id}")
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar pagamento ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao deletar pagamento")
