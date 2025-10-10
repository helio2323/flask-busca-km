from pydantic import BaseModel
from typing import List, Union
from decimal import Decimal

class RouteCalculate(BaseModel):
    origem: str
    destino: str

class RouteMultipleCalculate(BaseModel):
    origem: str
    destinos: List[str]

class RouteResponse(BaseModel):
    origem: str
    destino: str
    distance: Union[Decimal, str]
    pedagios: Union[Decimal, str]

class RouteMultipleResponse(BaseModel):
    origem: str
    destinos: List[str]
    total_distance: Union[Decimal, str]
    total_pedagios: Union[Decimal, str]
    tempo_estimado: Union[Decimal, str, None] = None
    combustivel_estimado: Union[Decimal, str, None] = None
    fonte: str = "API Rotas Brasil"

class RouteBatchResponse(BaseModel):
    resultados: List[RouteResponse]
