from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GrupoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class GrupoCreate(GrupoBase):
    pass

class GrupoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None

class GrupoResponse(GrupoBase):
    id: int
    data_criacao: datetime
    total_rotas: int
    total_distancia: float
    total_pedagios: float
    status: str
    
    model_config = {"from_attributes": True}

class GrupoList(BaseModel):
    grupos: list[GrupoResponse]
    total: int

class GrupoStats(BaseModel):
    total_grupos: int
    total_rotas: int
    total_distancia: float
    total_pedagios: float
    grupos_ativos: int
