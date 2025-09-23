from fastapi import APIRouter, HTTPException
from ..services.route_service import RouteService

router = APIRouter(prefix="/cache", tags=["cache"])

@router.get("/stats")
async def get_cache_stats():
    """Retorna estatísticas do cache"""
    try:
        route_service = RouteService()
        
        # Limpar caches expirados
        import time
        agora = time.time()
        
        # Limpar coordenadas expiradas (7 dias)
        coordenadas_expiradas = [k for k, v in route_service.cache_coordenadas.items() 
                               if agora - v['timestamp'] > (168 * 3600)]
        for k in coordenadas_expiradas:
            del route_service.cache_coordenadas[k]
        
        # Limpar rotas expiradas (6 horas)
        rotas_expiradas = [k for k, v in route_service.cache_rotas.items() 
                          if agora - v['timestamp'] > (6 * 3600)]
        for k in rotas_expiradas:
            del route_service.cache_rotas[k]
        
        return {
            "coordenadas_cache": len(route_service.cache_coordenadas),
            "rotas_cache": len(route_service.cache_rotas),
            "sugestoes_cache": len(route_service.cache_sugestoes),
            "total_entradas": len(route_service.cache_coordenadas) + len(route_service.cache_rotas) + len(route_service.cache_sugestoes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas do cache: {str(e)}")

@router.post("/clear")
async def clear_cache():
    """Limpa todo o cache"""
    try:
        route_service = RouteService()
        route_service.cache_coordenadas.clear()
        route_service.cache_rotas.clear()
        route_service.cache_sugestoes.clear()
        
        return {"message": "Cache limpo com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar cache: {str(e)}")
