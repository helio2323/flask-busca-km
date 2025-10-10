import asyncio
import hashlib
import time
import requests
import json
from typing import Optional, List, Dict, Any
# Removido geopy - agora usando apenas RotasBrasilService
from decimal import Decimal
from ..core.config import settings
from .cache_service import cache_service
from .webscraping_service import WebScrapingService
from .rotas_brasil_service import RotasBrasilService

class RouteService:
    def __init__(self):
        self.webscraping_service = WebScrapingService()
        self.rotas_brasil_service = RotasBrasilService()  # Serviço principal
    
    async def obter_latitude_longitude(self, cidade: str) -> tuple[Optional[float], Optional[float]]:
        """Obtém latitude e longitude de uma cidade usando sempre a API do Rotas Brasil"""
        try:
            # Normalizar formato da cidade (pipe para vírgula, manter vírgulas)
            cidade_normalizada = cidade.replace('|', ',').strip()
            
            # SEMPRE usar a API do Rotas Brasil - cache desabilitado
            print(f"Buscando coordenadas via API Rotas Brasil: {cidade_normalizada}")
            coordenadas = await self.rotas_brasil_service.buscar_coordenadas_cidade(cidade_normalizada)
            
            if coordenadas:
                lat, lon = coordenadas
                print(f"Coordenadas encontradas: {lat}, {lon}")
                return lat, lon
            else:
                print(f"Coordenadas não encontradas para: {cidade_normalizada}")
                return None, None
        except Exception as e:
            print(f"Erro ao obter coordenadas para {cidade}: {e}")
            return None, None
    
    async def criar_string_pontos_por_cidades(self, cidades: List[str]) -> Optional[str]:
        """Cria string de pontos para a API de rotas usando sempre a API do Rotas Brasil"""
        print(f"🔗 Criando string de pontos para {len(cidades)} cidades...")
        coordenadas = []
        for i, cidade in enumerate(cidades, 1):
            print(f"Processando cidade {i}/{len(cidades)}: {cidade}")
            latitude, longitude = await self.obter_latitude_longitude(cidade)
            if latitude is not None and longitude is not None:
                coordenadas.append((latitude, longitude))
                print(f"Coordenada adicionada: {latitude}, {longitude}")
            else:
                print(f"Coordenadas não encontradas para: {cidade}")
                return None
        
        if len(coordenadas) < 2:
            print(f"Mínimo de 2 coordenadas necessárias, encontradas: {len(coordenadas)}")
            return None
            
        pontos = ""
        for coordenada in coordenadas:
            pontos += f"{coordenada[1]},{coordenada[0]};"
        pontos_final = pontos[:-1]  # Remove o último ponto e vírgula desnecessários
        print(f"String de pontos criada: {pontos_final}")
        return pontos_final
    
    async def chamar_api_rotas_brasil(self, url: str) -> Dict[str, Any]:
        """Chama a API do Rotas Brasil"""
        try:
            print(f"Fazendo requisição para API do Rotas Brasil...")
            headers = {
                'authority': 'rotasbrasil.com.br',
                'accept': '*/*',
                'accept-language': 'pt-BR,pt;q=0.7',
                'cookie': 'RBNOTIFICATION=true; RBCOUNTNOTIFICATION=19; JSESSIONID=DD991B79A608CF2F40C3DDD0428DD789; veiculo=4; eixo=6; precoCombustivel=; consumo=',
                'referer': 'https://rotasbrasil.com.br/',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            print(f"Resposta recebida da API (status: {response.status_code})")
            return response.json()
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout na API - tente novamente")
            raise Exception("Timeout na API - tente novamente")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            raise Exception(f"Erro na requisição: {str(e)}")
        except json.JSONDecodeError:
            print(f"Resposta inválida da API")
            raise Exception("Resposta inválida da API")
    
    async def calcular_pedagio(self, loads: List[List]) -> float:
        """Calcula o total de pedágios"""
        try:
            total_pedagio = 0
            for sublista in loads:
                if len(sublista) > 8:
                    # A nona posição de cada sublista contém o valor do pedágio
                    total_pedagio += float(sublista[8])  # Somando os valores do pedágio
            return total_pedagio
        except (IndexError, ValueError, TypeError) as e:
            print(f"Erro ao calcular pedágio: {e}")
            return 0.0
    
    async def processar_rota(self, origem: str, destino: str) -> Dict[str, Any]:
        """Processa uma rota individual usando sempre a API do Rotas Brasil"""
        try:
            print(f"🚀 Processando rota: {origem} → {destino}")
            
            # SEMPRE usar a API do Rotas Brasil - cache desabilitado
            resultado = await self.rotas_brasil_service.processar_rota(origem, destino)
            
            if resultado and resultado.get('distance', 0) > 0:
                print(f"✅ Rota processada via API Rotas Brasil: {resultado['distance']} km, R$ {resultado['pedagios']}")
                return resultado
            else:
                print(f"❌ API Rotas Brasil falhou, tentando webscraping...")
                # Fallback para webscraping se a API falhar
                resultado_webscraping = await self.webscraping_service.processar_rota(origem, destino)
                if resultado_webscraping:
                    print(f"✅ Rota processada via webscraping: {resultado_webscraping['distance']} km, R$ {resultado_webscraping['pedagios']}")
                    return resultado_webscraping
                else:
                    print(f"❌ Todas as fontes falharam para: {origem} → {destino}")
                    return {
                        "origem": origem,
                        "destino": destino,
                        "distance": 0,
                        "pedagios": 0,
                        "duration": 0,
                        "fonte": "erro",
                        "erro": "Todas as fontes falharam"
                    }
                    
        except Exception as e:
            print(f"❌ Erro ao processar rota {origem} → {destino}: {e}")
            return {
                "origem": origem,
                "destino": destino,
                "distance": 0,
                "pedagios": 0,
                "duration": 0,
                "fonte": "erro",
                "erro": str(e)
            }
    
    async def processar_rota_multipla(self, origem: str, destinos: List[str]) -> Dict[str, Any]:
        """Processa uma rota com múltiplos destinos usando sempre a API do Rotas Brasil"""
        try:
            print(f"🚀 Processando rota múltipla: {origem} → {destinos}")
            
            # SEMPRE usar a API do Rotas Brasil - cache desabilitado
            resultado = await self.rotas_brasil_service.processar_rota_multipla(origem, destinos)
            
            if resultado and resultado.get('total_distance', 0) > 0:
                print(f"✅ Rota múltipla processada via API Rotas Brasil: {resultado['total_distance']} km, R$ {resultado['total_pedagios']}")
                return resultado
            else:
                print(f"❌ API Rotas Brasil falhou para rota múltipla, tentando webscraping...")
                # Fallback para webscraping se a API falhar
                resultado_webscraping = await self.webscraping_service.processar_rota_multipla(origem, destinos)
                if resultado_webscraping:
                    print(f"✅ Rota múltipla processada via webscraping: {resultado_webscraping.get('total_distance', resultado_webscraping.get('distance', 0))} km, R$ {resultado_webscraping.get('total_pedagios', resultado_webscraping.get('pedagios', 0))}")
                    return resultado_webscraping
                else:
                    print(f"❌ Todas as fontes falharam para rota múltipla: {origem} → {destinos}")
                    return {
                        "origem": origem,
                        "destinos": destinos,
                        "total_distance": 0,
                        "total_pedagios": 0,
                        "total_duration": 0,
                        "fonte": "erro",
                        "erro": "Todas as fontes falharam"
                    }
                    
        except Exception as e:
            print(f"❌ Erro ao processar rota múltipla {origem} → {destinos}: {e}")
            return {
                "origem": origem,
                "destinos": destinos,
                "distance": 0,
                "pedagios": 0,
                "duration": 0,
                "fonte": "erro",
                "erro": str(e)
            }
