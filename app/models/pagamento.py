from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class StatusPagamento(str, Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    CONCLUIDO = "concluido"
    FALHA = "falha"
    CANCELADO = "cancelado"

class Pagamento(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "valor": 150.50,
                "descricao": "Pagamento de serviços",
                "status": "pendente"
            }
        }
    )
    
    id: Optional[int] = Field(None, description="ID do pagamento (gerado automaticamente)")
    valor: float = Field(..., gt=0, description="Valor do pagamento (deve ser maior que 0)")
    descricao: str = Field(..., min_length=1, max_length=500, description="Descrição do pagamento")
    status: StatusPagamento = Field(default=StatusPagamento.PENDENTE, description="Status do pagamento")
