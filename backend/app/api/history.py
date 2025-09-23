from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from ..core.database import get_db
from ..schemas.consulta import ConsultaList, ConsultaResponse
from ..models.consulta import Consulta

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/", response_model=ConsultaList)
async def get_history(
    page: int = Query(1, ge=1),
    size: int = Query(100, ge=1, le=1000),
    tipo_consulta: Optional[str] = Query(None),
    grupo_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Retorna histórico de consultas"""
    try:
        query = db.query(Consulta)
        
        # Filtros
        if tipo_consulta:
            query = query.filter(Consulta.tipo_consulta == tipo_consulta)
        if grupo_id:
            query = query.filter(Consulta.grupo_id == grupo_id)
        
        # Paginação
        total = query.count()
        consultas = query.order_by(desc(Consulta.data_consulta)).offset((page - 1) * size).limit(size).all()
        
        return ConsultaList(
            consultas=[ConsultaResponse.from_orm(consulta) for consulta in consultas],
            total=total,
            page=page,
            size=size
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter histórico: {str(e)}")

@router.delete("/{consulta_id}")
async def delete_consulta(consulta_id: int, db: Session = Depends(get_db)):
    """Deleta uma consulta do histórico"""
    try:
        consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
        if not consulta:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        
        db.delete(consulta)
        db.commit()
        
        return {"message": "Consulta deletada com sucesso"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar consulta: {str(e)}")

@router.delete("/")
async def clear_history(db: Session = Depends(get_db)):
    """Limpa todo o histórico"""
    try:
        db.query(Consulta).delete()
        db.commit()
        
        return {"message": "Histórico limpo com sucesso"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar histórico: {str(e)}")
