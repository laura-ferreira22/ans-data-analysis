from pydantic import BaseModel
from typing import Optional, List

class OperadoraOut(BaseModel):
    cnpj: str
    razao_social: str
    uf: Optional[str] = None
    modalidade: Optional[str] = None

class DespesaOut(BaseModel):
    ano: int
    trimestre: str
    valor_despesas: float

class EstatisticasUFOut(BaseModel):
    uf: str
    total_despesas: float
    media_por_operadora: float

class PaginatedOperadoras(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[OperadoraOut]
