import asyncio
import hashlib
import time
import requests
import json
import urllib.parse
from typing import Optional, List, Dict, Any, Tuple
from ..core.config import settings
from .cache_service import cache_service


class RotasBrasilService:
    """
    Serviço para integração com as APIs do Rotas Brasil
    """
    
    def __init__(self):
        self.cache_coordenadas = {}
        self.cache_rotas = {}
        self.base_url_autocomplete = "https://rotasbrasil.com.br/apiRotas/autocomplete/"
        self.base_url_routes = "https://rotasbrasil.com.br/roterizador/buscaRota/"
        
        # Headers padrão para as requisições
        self.headers = {
            "accept": "*/*",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://rotasbrasil.com.br/",
            "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
    
    def gerar_chave_cache(self, texto: str) -> str:
        """Gera uma chave única para o cache usando hash MD5"""
        return hashlib.md5(texto.encode('utf-8')).hexdigest()
    
    def cache_expirado(self, timestamp: float, duracao_horas: int) -> bool:
        """Verifica se o cache expirou"""
        return time.time() - timestamp > (duracao_horas * 3600)
    
    async def buscar_sugestoes_cidade(self, termo: str) -> List[Dict[str, Any]]:
        """Busca sugestões de cidades usando a API de autocomplete do Rotas Brasil"""
        try:
            # Formatar termo para a API
            termo_formatado = termo.strip().upper()
            
            # Fazer requisição para a API de autocomplete
            url = "https://rotasbrasil.com.br/api/autocomplete"
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Content-Type": "application/json",
                "Origin": "https://rotasbrasil.com.br",
                "Pragma": "no-cache",
                "Referer": "https://rotasbrasil.com.br/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            params = {
                "q": termo_formatado,
                "limit": 10
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                
                if isinstance(data, list):
                    suggestions = []
                    for item in data:
                        if isinstance(item, dict) and 'nome' in item:
                            suggestions.append({
                                "nome": item.get('nome', ''),
                                "endereco_completo": item.get('endereco_completo', item.get('nome', '')),
                                "latitude": item.get('lat', 0.0),
                                "longitude": item.get('lon', 0.0)
                            })
                    return suggestions
                else:
                    return []
                    
        except Exception as e:
            print(f"Erro ao buscar sugestões para '{termo}': {e}")
            return []

    async def buscar_cidade_completa(self, cidade_completa: str) -> Optional[Dict[str, Any]]:
        """
        Busca uma cidade completa usando a API de autocomplete do Rotas Brasil
        
        Args:
            cidade_completa: Cidade no formato "Cidade, Estado, BR"
            
        Returns:
            Dict com {'nome_correto': str, 'estado': str, 'lat': float, 'lon': float} ou None
        """
        try:
            # Verificar cache primeiro
            chave_cache = self.gerar_chave_cache(f"cidade_completa_{cidade_completa}")
            if chave_cache in self.cache_coordenadas:
                dados_cache = self.cache_coordenadas[chave_cache]
                if not self.cache_expirado(dados_cache['timestamp'], 24):  # Cache válido por 24 horas
                    return dados_cache['cidade_completa']
                else:
                    del self.cache_coordenadas[chave_cache]
            
            print(f"Buscando cidade completa: {cidade_completa}")
            
            # Extrair cidade e estado para a busca
            partes = cidade_completa.split(',')
            cidade_busca = partes[0].strip()
            estado_busca = partes[1].strip() if len(partes) > 1 else ""
            
            # Enviar cidade + estado para o autocomplete (formato: "Cidade Estado")
            if estado_busca:
                query_busca = f"{cidade_busca} {estado_busca}"
            else:
                query_busca = cidade_busca
            
            print(f"Buscando no autocomplete: '{query_busca}'")
            
            # Fazer requisição para a API de autocomplete
            url = f"{self.base_url_autocomplete}?q={urllib.parse.quote(query_busca)}&limit=10"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Procurar a cidade correta
            for result in data:
                cidade_result = result.get('cidade', '') or ''
                estado_result = result.get('estado', '') or ''
                lat = result.get('lat')
                lon = result.get('lon')
                
                # Verificar se temos dados válidos (coordenadas são obrigatórias)
                if not lat or not lon:
                    continue
                
                # Se cidade_result está vazio, usar a cidade_busca original
                if not cidade_result:
                    cidade_result = cidade_busca
                
                # Tentar fazer match com a cidade
                cidade_upper = cidade_busca.upper().strip()
                cidade_result_upper = cidade_result.upper().strip()
                
                # Match mais flexível - verificar se a cidade buscada está contida no resultado
                if cidade_upper in cidade_result_upper or cidade_result_upper in cidade_upper:
                    cidade_completa_result = {
                        'nome_correto': cidade_result,
                        'estado': estado_result,
                        'lat': lat,
                        'lon': lon
                    }
                    # Salvar no cache
                    self.cache_coordenadas[chave_cache] = {
                        'cidade_completa': cidade_completa_result,
                        'timestamp': time.time()
                    }
                    print(f"Cidade encontrada: {cidade_result}, {estado_result} ({lat}, {lon})")
                    return cidade_completa_result
            
            print(f"Cidade não encontrada: {cidade_completa}")
            return None
            
        except Exception as e:
            print(f"Erro ao buscar cidade completa {cidade_completa}: {e}")
            return None
    async def buscar_coordenadas_cidade(self, cidade: str, estado: str = None) -> Optional[Tuple[float, float]]:
        """
        Busca coordenadas de uma cidade usando a API de autocomplete do Rotas Brasil
        
        Args:
            cidade: Nome da cidade
            estado: Nome do estado (opcional)
            
        Returns:
            Tuple com (latitude, longitude) ou None se não encontrado
        """
        cidade_completa = await self.buscar_cidade_completa(cidade, estado)
        if cidade_completa:
            return (cidade_completa['lat'], cidade_completa['lon'])
        return None
    
    async def calcular_rota_com_coordenadas(self, origem: str, destino: str, 
                                          coordenadas_origem: Tuple[float, float], 
                                          coordenadas_destino: Tuple[float, float]) -> Dict[str, Any]:
        """
        Calcula rota usando coordenadas específicas
        
        Args:
            origem: Nome da cidade de origem
            destino: Nome da cidade de destino
            coordenadas_origem: Tuple (lat, lon) da origem
            coordenadas_destino: Tuple (lat, lon) do destino
            
        Returns:
            Dicionário com informações da rota
        """
        try:
            # Verificar cache primeiro
            chave_cache = self.gerar_chave_cache(f"{origem}->{destino}")
            if chave_cache in self.cache_rotas:
                dados_cache = self.cache_rotas[chave_cache]
                if not self.cache_expirado(dados_cache['timestamp'], 6):  # Cache válido por 6 horas
                    return dados_cache['resultado']
                else:
                    del self.cache_rotas[chave_cache]
            
            # Construir URL da API de rotas
            pontos = f"{coordenadas_origem[1]},{coordenadas_origem[0]};{coordenadas_destino[1]},{coordenadas_destino[0]}"
            origem_param = urllib.parse.quote(origem)
            destino_param = urllib.parse.quote(destino)
            
            url = f"{self.base_url_routes}?pontos={pontos}&alternatives=true&eixos=2&veiculo=1&origem={origem_param}&destino={destino_param}&st=false&combustivel=&consumo=&evitarPedagio=false&recaptchaRespostaCliente=0cAFcWeA5T_9JrEsMPEqBuFiC_-asCjKx1VknRHQCh8XLjG1UTq5qP_OOahYcjSU7t8QzsjAL1P8cFjW1a_dt75dEZmw2AcooV9GCZTx9CBfWuWTmBnFpntKdYPrXRYUAUZRElta40W3aO9z6u2Y1QSnvtP0jm220QvAuhov5L1Bc3tvvPncrlcoOGzWo-55KDRU2n6qQkqY__IwfUUQAzEe0PZ9EqdofPmGhsqnBeizp6ub7m2PhPl1QhtjOhguT7JTu0RIJjuRUvu_hQSrGLgQrk26b5dLThLzwONwt4CQijvhyfniG6Jz3fxW2omiLl_mu0jtfpZLtfRGbV_-B-qBw2lJo0FEINc4LYOOfocsW94SwFRP5x81nUaW6p3OW1d2tpFm2f6vz3t2NUJ8oscv3jA43HodkU0S5S5S-itV-1J0x_gspu8tWfoCNPzWRnz-YtDm0Cc6kPG6l9H8RDXeL554Zhayoy83YM1qQiZ85R-YoHtNK14wgADKtLk22LTV3KXbDd-69ssh8OBAFglJF_LB0O14iM2t-vW4b89JDqlTQWAbZl_fR-IwCM_G0bUcKNh1h4rvuQhugsDAAmkD3xnjvUm_WQulADF-fXov4i7ngmvr3oAAclciZvT2qRkOydnPz6XSSCnsfMY4ENL2rG9H0Tmy2IlvnhIp1hIAGk8xUFS78-zJTt3PjagtS2RkNta_rTLAj9uglIW_a9FSAxAF-wG4qsmAWQC1K-IKZOZFj_x0hhyYzrPo1kmziQiHHLBhXh-KHD&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2025-10-09"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extrair informações da rota
            if 'routes' in data and len(data['routes']) > 0:
                route = data['routes'][0]  # Primeira rota
                distance = route.get('distance', 0) / 1000  # Converter de metros para km
                duration = route.get('duration', 0) / 60  # Converter de segundos para minutos
                
                # Calcular pedágios da API
                pedagios = 0.0
                if 'pedagios' in route and route['pedagios']:
                    # Se há pedágios na resposta, calcular o total
                    try:
                        if isinstance(route['pedagios'], list):
                            # Estrutura: cada pedágio é uma lista com 14 elementos
                            # Posição 8: valor do pedágio (número direto)
                            for pedagio in route['pedagios']:
                                if isinstance(pedagio, list) and len(pedagio) > 8:
                                    valor_float = float(pedagio[8])  # Posição 8: valor do pedágio
                                    pedagios += valor_float
                                    print(f"Pedágio encontrado: {pedagio[5]} - R$ {valor_float:.2f}")
                        elif isinstance(route['pedagios'], (int, float)):
                            # Se é um número direto
                            pedagios = float(route['pedagios'])
                    except (ValueError, TypeError, IndexError) as e:
                        print(f"Erro ao processar pedágios: {e}")
                        pedagios = 0.0
                
                print(f"Total de pedágios calculados: R$ {pedagios}")
                
                resultado = {
                    "origem": origem,
                    "destino": destino,
                    "distance": round(distance, 1),
                    "pedagios": pedagios,
                    "duration": round(duration, 1),
                    "fonte": "rotas_brasil_api",
                    "raw_data": data
                }
                
                # Salvar no cache
                self.cache_rotas[chave_cache] = {
                    'resultado': resultado,
                    'timestamp': time.time()
                }
                
                return resultado
            else:
                return {
                    "origem": origem,
                    "destino": destino,
                    "distance": 0,
                    "pedagios": 0,
                    "duration": 0,
                    "fonte": "rotas_brasil_api_erro",
                    "erro": "Nenhuma rota encontrada"
                }
                
        except Exception as e:
            print(f"Erro ao calcular rota {origem} -> {destino}: {e}")
            return {
                "origem": origem,
                "destino": destino,
                "distance": 0,
                "pedagios": 0,
                "duration": 0,
                "fonte": "rotas_brasil_api_erro",
                "erro": str(e)
            }
    
    async def processar_rota(self, origem: str, destino: str) -> Dict[str, Any]:
        """
        Processa uma rota individual usando as APIs do Rotas Brasil
        
        Args:
            origem: Cidade de origem no formato "Cidade, Estado, BR"
            destino: Cidade de destino no formato "Cidade, Estado, BR"
            
        Returns:
            Dicionário com informações da rota
        """
        try:
            print(f"Processando rota: {origem} -> {destino}")
            
            # Extrair cidade e estado da origem
            origem_parts = origem.split(',')
            if len(origem_parts) >= 2:
                cidade_origem = origem_parts[0].strip()
                estado_origem = origem_parts[1].strip()
            else:
                cidade_origem = origem.strip()
                estado_origem = None
            
            # Extrair cidade e estado do destino
            destino_parts = destino.split(',')
            if len(destino_parts) >= 2:
                cidade_destino = destino_parts[0].strip()
                estado_destino = destino_parts[1].strip()
            else:
                cidade_destino = destino.strip()
                estado_destino = None
            
            # BUSCAR CIDADE DE ORIGEM usando API de autocomplete
            # Concatenar município + estado no formato correto: "Campinas, Sao Paulo, BR"
            cidade_origem_formatada = f"{cidade_origem}, {estado_origem}, BR" if estado_origem else f"{cidade_origem}, BR"
            print(f"Buscando cidade de origem: {cidade_origem_formatada}")
            cidade_origem_completa = await self.buscar_cidade_completa(cidade_origem_formatada)
            if not cidade_origem_completa:
                return {
                    "origem": origem,
                    "destino": destino,
                    "distance": 0,
                    "pedagios": 0,
                    "duration": 0,
                    "fonte": "rotas_brasil_api_erro",
                    "erro": f"Cidade de origem não encontrada: {cidade_origem_formatada}"
                }
            
            # BUSCAR CIDADE DE DESTINO usando API de autocomplete
            # Concatenar município + estado no formato correto: "Adamantina, Sao Paulo, BR"
            cidade_destino_formatada = f"{cidade_destino}, {estado_destino}, BR" if estado_destino else f"{cidade_destino}, BR"
            print(f"Buscando cidade de destino: {cidade_destino_formatada}")
            cidade_destino_completa = await self.buscar_cidade_completa(cidade_destino_formatada)
            if not cidade_destino_completa:
                return {
                    "origem": origem,
                    "destino": destino,
                    "distance": 0,
                    "pedagios": 0,
                    "duration": 0,
                    "fonte": "rotas_brasil_api_erro",
                    "erro": f"Cidade de destino não encontrada: {cidade_destino_formatada}"
                }
            
            # Usar os nomes corretos das cidades para calcular a rota
            origem_correta = f"{cidade_origem_completa['nome_correto']}, {cidade_origem_completa['estado']}, BR"
            destino_correto = f"{cidade_destino_completa['nome_correto']}, {cidade_destino_completa['estado']}, BR"
            
            print(f"Usando nomes corretos: {origem_correta} -> {destino_correto}")
            
            # Calcular rota usando as coordenadas corretas
            return await self.calcular_rota_com_coordenadas(
                origem_correta,
                destino_correto,
                (cidade_origem_completa['lat'], cidade_origem_completa['lon']),
                (cidade_destino_completa['lat'], cidade_destino_completa['lon'])
            )
            
        except Exception as e:
            print(f"Erro ao processar rota {origem} -> {destino}: {e}")
            return {
                "origem": origem,
                "destino": destino,
                "distance": 0,
                "pedagios": 0,
                "duration": 0,
                "fonte": "rotas_brasil_api_erro",
                "erro": str(e)
            }
    
    async def processar_rota_multipla(self, origem: str, destinos: List[str]) -> Dict[str, Any]:
        """
        Processa múltiplas rotas a partir de uma origem
        
        Args:
            origem: Cidade de origem
            destinos: Lista de cidades de destino
            
        Returns:
            Dicionário com informações das rotas
        """
        try:
            resultados = []
            total_distance = 0
            total_pedagios = 0
            total_duration = 0
            
            for destino in destinos:
                resultado = await self.processar_rota(origem, destino)
                resultados.append(resultado)
                
                if resultado.get("distance", 0) > 0:
                    total_distance += resultado["distance"]
                    total_pedagios += resultado["pedagios"]
                    total_duration += resultado["duration"]
            
            return {
                "origem": origem,
                "destinos": destinos,
                "total_distance": round(total_distance, 1),
                "total_pedagios": round(total_pedagios, 1),
                "total_duration": round(total_duration, 1),
                "rotas": resultados,
                "fonte": "rotas_brasil_api_multipla"
            }
            
        except Exception as e:
            print(f"Erro ao processar rotas múltiplas: {e}")
            return {
                "origem": origem,
                "destinos": destinos,
                "total_distance": 0,
                "total_pedagios": 0,
                "total_duration": 0,
                "rotas": [],
                "fonte": "rotas_brasil_api_erro",
                "erro": str(e)
            }
