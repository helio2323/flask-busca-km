from sqlalchemy import Column, Integer, String, DateTime, Index, JSON
from sqlalchemy.sql import func
from ..core.database import Base

class CacheRota(Base):
    __tablename__ = "cache_rotas"
    
    id = Column(Integer, primary_key=True, index=True)
    chave_rota = Column(String(255), unique=True, nullable=False, index=True)
    resultado = Column(JSON, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_expiracao = Column(DateTime(timezone=True), nullable=False)
    
    # Índice para busca por expiração
    __table_args__ = (
        Index('idx_cache_rotas_expiracao', 'data_expiracao'),
    )
