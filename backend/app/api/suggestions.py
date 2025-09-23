from fastapi import APIRouter, HTTPException
from ..schemas.suggestion import SuggestionResponse
from ..services.route_service import RouteService

router = APIRouter(prefix="/suggestions", tags=["suggestions"])

@router.get("/{termo}", response_model=SuggestionResponse)
async def get_suggestions(termo: str):
    """Retorna sugestões de cidades baseado no termo digitado"""
    try:
        if len(termo) < 2:
            return SuggestionResponse(sugestoes=[])
        
        route_service = RouteService()
        sugestoes = await route_service.buscar_sugestoes_cidade(termo)
        return SuggestionResponse(sugestoes=sugestoes)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter sugestões: {str(e)}")
