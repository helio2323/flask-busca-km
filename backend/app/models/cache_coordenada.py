from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Index
from sqlalchemy.sql import func
from ..core.database import Base

class CacheCoordenada(Base):
    __tablename__ = "cache_coordenadas"
    
    id = Column(Integer, primary_key=True, index=True)
    cidade = Column(String(255), unique=True, nullable=False, index=True)
    latitude = Column(DECIMAL(10, 8), nullable=False)
    longitude = Column(DECIMAL(11, 8), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_expiracao = Column(DateTime(timezone=True), nullable=False)
    
    # Índice para busca por expiração
    __table_args__ = (
        Index('idx_cache_coordenadas_expiracao', 'data_expiracao'),
    )
