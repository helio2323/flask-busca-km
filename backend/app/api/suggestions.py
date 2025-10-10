from fastapi import APIRouter, HTTPException, Query
from ..schemas.suggestion import SuggestionResponse
from ..services.rotas_brasil_service import RotasBrasilService

router = APIRouter(prefix="/suggestions", tags=["suggestions"])

@router.get("/", response_model=SuggestionResponse)
async def get_suggestions(termo: str = Query(..., description="Termo de busca para cidades")):
    """Retorna sugestões de cidades baseado no termo digitado"""
    try:
        if len(termo) < 3:
            return SuggestionResponse(sugestoes=[])
        
        # Temporariamente retornar sugestões mock para debug
        mock_suggestions = [
            {
                "nome": f"{termo} - Cidade 1",
                "endereco_completo": f"{termo}, São Paulo, BR",
                "latitude": -23.5505,
                "longitude": -46.6333
            },
            {
                "nome": f"{termo} - Cidade 2", 
                "endereco_completo": f"{termo}, Rio de Janeiro, BR",
                "latitude": -22.9068,
                "longitude": -43.1729
            }
        ]
        
        return SuggestionResponse(sugestoes=mock_suggestions)
        
        # Código original comentado para debug
        # rotas_brasil_service = RotasBrasilService()
        # suggestions = await rotas_brasil_service.buscar_sugestoes_cidade(termo)
        # return SuggestionResponse(sugestoes=suggestions)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter sugestões: {str(e)}")
