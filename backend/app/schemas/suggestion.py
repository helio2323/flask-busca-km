from pydantic import BaseModel
from typing import List
from decimal import Decimal

class SuggestionItem(BaseModel):
    nome: str
    endereco_completo: str
    latitude: Decimal
    longitude: Decimal

class SuggestionResponse(BaseModel):
    sugestoes: List[SuggestionItem]
