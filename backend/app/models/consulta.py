from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Consulta(Base):
    __tablename__ = "consultas"
    
    id = Column(Integer, primary_key=True, index=True)
    planilha_id = Column(String(50), nullable=True)  # ID da planilha original
    origem = Column(String(255), nullable=False)
    destino = Column(String(255), nullable=False)
    uf_origem = Column(String(10), nullable=True)  # UF da origem
    uf_destino = Column(String(10), nullable=True)  # UF do destino
    distancia = Column(DECIMAL(10, 2), nullable=True)
    pedagios = Column(DECIMAL(10, 2), nullable=True)
    ip_address = Column(String(45), nullable=True)
    data_consulta = Column(DateTime(timezone=True), server_default=func.now())
    tipo_consulta = Column(String(20), default="individual")
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=True)
    cache_hit = Column(String(10), nullable=True)  # 'true' se veio do cache, 'false' se da API
    
    # Relacionamento
    grupo = relationship("Grupo", back_populates="consultas")
