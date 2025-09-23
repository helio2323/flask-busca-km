from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Grupo(Base):
    __tablename__ = "grupos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    total_rotas = Column(Integer, default=0)
    total_distancia = Column(Float, default=0.0)
    total_pedagios = Column(Float, default=0.0)
    status = Column(String(50), default="ativo")  # ativo, arquivado, excluido
    
    # Relacionamentos
    consultas = relationship("Consulta", back_populates="grupo")
    upload_errors = relationship("UploadError", back_populates="grupo")
