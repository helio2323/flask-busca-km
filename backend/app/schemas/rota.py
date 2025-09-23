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

class RouteBatchResponse(BaseModel):
    resultados: List[RouteResponse]
