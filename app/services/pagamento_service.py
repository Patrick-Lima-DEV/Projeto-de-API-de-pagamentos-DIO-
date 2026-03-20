import logging
from copy import deepcopy

logger = logging.getLogger(__name__)

pagamentos = []

def add_pagamento(pagamento):
    """Adiciona um novo pagamento à lista"""
    pagamento_dict = pagamento.model_dump()
    pagamento_dict["id"] = len(pagamentos) + 1
    pagamentos.append(pagamento_dict)
    logger.debug(f"Pagamento adicionado com ID {pagamento_dict['id']}")
    return pagamento_dict

def update_pagamento(id: int, pagamento):
    """Atualiza um pagamento existente"""
    for i, p in enumerate(pagamentos):
        if p["id"] == id:
            pagamento_dict = pagamento.model_dump()
            pagamento_dict["id"] = id  # Preserva o ID original
            pagamentos[i] = pagamento_dict
            logger.debug(f"Pagamento ID {id} atualizado")
            return pagamento_dict
    return {"erro": "Pagamento não encontrado"}

def delete_pagamento(id: int):
    """Deleta um pagamento existente"""
    for i, p in enumerate(pagamentos):
        if p["id"] == id:
            pagamentos.pop(i)
            logger.debug(f"Pagamento ID {id} removido")
            return {"msg": "Pagamento removido", "id": id}
    return {"erro": "Pagamento não encontrado"}
