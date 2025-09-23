"""
Serviço de cache para rotas calculadas
"""
import json
import hashlib
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from ..models.consulta import Consulta

class CacheService:
    def __init__(self):
        self.cache = {}  # Cache em memória para consultas rápidas
    
    def _gerar_chave_cache(self, origem: str, destino: str) -> str:
        """Gera uma chave única para a rota no cache"""
        rota_normalizada = f"{origem.strip().lower()}|{destino.strip().lower()}"
        return hashlib.md5(rota_normalizada.encode()).hexdigest()
    
    def buscar_no_cache(self, origem: str, destino: str, db: Session) -> Optional[Dict[str, Any]]:
        """
        Busca uma rota no cache (banco de dados)
        Retorna os dados da rota se encontrada, None caso contrário
        """
        try:
            # Limpar o destino para busca (remover [UPLOAD:...] se existir)
            destino_limpo = destino
            if "[UPLOAD:" in destino_limpo:
                destino_limpo = destino_limpo.split(" [UPLOAD:")[0]
            
            # Buscar rota no banco que tenha distância e pedágios calculados
            # Buscar por destino limpo ou destino com qualquer upload_id
            consulta = db.query(Consulta).filter(
                Consulta.origem == origem,
                Consulta.distancia.isnot(None),
                Consulta.pedagios.isnot(None),
                Consulta.distancia > 0,  # Garantir que distância é válida
                Consulta.pedagios >= 0   # Garantir que pedágios é válido
            ).filter(
                # Buscar por destino exato ou destino que contenha a cidade (sem upload_id)
                (Consulta.destino == destino_limpo) | 
                (Consulta.destino.like(f"{destino_limpo} [UPLOAD:%"))
            ).order_by(Consulta.data_consulta.desc()).first()
            
            if consulta:
                print(f"🎯 Cache HIT: {origem} → {destino_limpo} (encontrado: {consulta.destino})")
                return {
                    "distancia": float(consulta.distancia),
                    "pedagios": float(consulta.pedagios),
                    "data_calculo": consulta.data_consulta,
                    "fonte": "cache"
                }
            else:
                print(f"❌ Cache MISS: {origem} → {destino_limpo}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao buscar no cache: {str(e)}")
            return None
    
    def salvar_no_cache(self, origem: str, destino: str, distancia: float, 
                       pedagios: float, planilha_id: str = None, 
                       grupo_id: int = None, ip_address: str = None, 
                       db: Session = None) -> bool:
        """
        Salva uma rota calculada no cache (banco de dados)
        """
        try:
            # Verificar se já existe uma consulta idêntica para evitar duplicatas
            consulta_existente = db.query(Consulta).filter(
                Consulta.origem == origem,
                Consulta.destino == destino,
                Consulta.distancia == distancia,
                Consulta.pedagios == pedagios
            ).first()
            
            if consulta_existente:
                print(f"⚠️ Rota já existe no cache: {origem} → {destino}")
                return True
            
            consulta = Consulta(
                planilha_id=planilha_id,
                origem=origem,
                destino=destino,
                distancia=distancia,
                pedagios=pedagios,
                ip_address=ip_address,
                tipo_consulta="batch",
                grupo_id=grupo_id,
                cache_hit="false"  # Esta é uma nova consulta, não veio do cache
            )
            
            db.add(consulta)
            db.commit()
            
            print(f"💾 Salvo no cache: {origem} → {destino} ({distancia}km, R${pedagios})")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar no cache: {str(e)}")
            db.rollback()
            return False
    
    def obter_estatisticas_cache(self, db: Session) -> Dict[str, Any]:
        """
        Retorna estatísticas do cache
        """
        try:
            total_rotas = db.query(Consulta).filter(
                Consulta.distancia.isnot(None),
                Consulta.pedagios.isnot(None)
            ).count()
            
            rotas_com_cache = db.query(Consulta).filter(
                Consulta.cache_hit == "true"
            ).count()
            
            return {
                "total_rotas_calculadas": total_rotas,
                "rotas_servidas_do_cache": rotas_com_cache,
                "taxa_cache_hit": (rotas_com_cache / total_rotas * 100) if total_rotas > 0 else 0
            }
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas do cache: {str(e)}")
            return {
                "total_rotas_calculadas": 0,
                "rotas_servidas_do_cache": 0,
                "taxa_cache_hit": 0
            }

# Instância global do serviço de cache
cache_service = CacheService()
