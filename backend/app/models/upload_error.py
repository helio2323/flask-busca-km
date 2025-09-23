from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime

class UploadError(Base):
    __tablename__ = "upload_errors"
    
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(String(50), nullable=False, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    planilha_id = Column(String(50), nullable=True)
    linha_index = Column(Integer, nullable=False)
    origem_original = Column(String(500), nullable=False)
    destino_original = Column(String(500), nullable=False)
    origem_corrigida = Column(String(500), nullable=True)
    destino_corrigido = Column(String(500), nullable=True)
    tipo_erro = Column(String(100), nullable=False)  # 'dados_invalidos', 'api_error', 'resultado_invalido', 'timeout', etc.
    mensagem_erro = Column(Text, nullable=True)
    status = Column(String(20), default="pendente")  # 'pendente', 'processando', 'sucesso', 'erro'
    criado_em = Column(DateTime, default=datetime.utcnow)
    processado_em = Column(DateTime, nullable=True)
    
    # Relacionamento com grupo
    grupo = relationship("Grupo", back_populates="upload_errors")
