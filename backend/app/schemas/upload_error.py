from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UploadErrorBase(BaseModel):
    upload_id: str
    grupo_id: int
    planilha_id: Optional[str] = None
    linha_index: int
    origem_original: str
    destino_original: str
    origem_corrigida: Optional[str] = None
    destino_corrigido: Optional[str] = None
    tipo_erro: str
    mensagem_erro: Optional[str] = None
    status: str = "pendente"

class UploadErrorCreate(UploadErrorBase):
    pass

class UploadErrorUpdate(BaseModel):
    origem_corrigida: Optional[str] = None
    destino_corrigido: Optional[str] = None
    status: Optional[str] = None

class UploadErrorResponse(UploadErrorBase):
    id: int
    criado_em: datetime
    processado_em: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ReprocessErrorRequest(BaseModel):
    origem_corrigida: str
    destino_corrigido: str
