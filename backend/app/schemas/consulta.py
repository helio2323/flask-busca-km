from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ConsultaBase(BaseModel):
    origem: str
    destino: str
    distancia: Optional[Decimal] = None
    pedagios: Optional[Decimal] = None
    ip_address: Optional[str] = None
    tipo_consulta: str = "individual"
    grupo_id: Optional[int] = None

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaResponse(ConsultaBase):
    id: int
    data_consulta: datetime
    
    class Config:
        from_attributes = True

class ConsultaList(BaseModel):
    consultas: list[ConsultaResponse]
    total: int
    page: int
    size: int
