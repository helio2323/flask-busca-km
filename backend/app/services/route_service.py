import asyncio
import hashlib
import time
import requests
import json
from typing import Optional, List, Dict, Any
from geopy.geocoders import Nominatim
from decimal import Decimal
from ..core.config import settings
from .cache_service import cache_service

class RouteService:
    def __init__(self):
        self.cache_coordenadas = {}
        self.cache_rotas = {}
        self.cache_sugestoes = {}
    
    def gerar_chave_cache(self, texto: str) -> str:
        """Gera uma chave única para o cache usando hash MD5"""
        return hashlib.md5(texto.encode('utf-8')).hexdigest()
    
    def cache_expirado(self, timestamp: float, duracao_horas: int) -> bool:
        """Verifica se o cache expirou"""
        return time.time() - timestamp > (duracao_horas * 3600)
    
    async def buscar_sugestoes_cidade(self, termo: str) -> List[Dict[str, Any]]:
        """Busca sugestões de cidades baseado no termo digitado"""
        try:
            # Verificar cache de sugestões (válido por 24 horas)
            chave_cache = self.gerar_chave_cache(f"sugestoes_{termo}")
            if chave_cache in self.cache_sugestoes:
                dados_cache = self.cache_sugestoes[chave_cache]
                if not self.cache_expirado(dados_cache['timestamp'], 24):  # 24 horas
                    return dados_cache['sugestoes']
                else:
                    del self.cache_sugestoes[chave_cache]
            
            geolocator = Nominatim(user_agent="calculadora_rotas_v2", timeout=10)
            
            # Buscar cidades no Brasil
            location = geolocator.geocode(f"{termo}, Brasil", exactly_one=False, limit=5)
            
            sugestoes = []
            if location:
                for loc in location:
                    if loc and loc.address:
                        # Extrair nome da cidade e estado
                        endereco = loc.address.split(', ')
                        if len(endereco) >= 2:
                            cidade_estado = f"{endereco[0]}, {endereco[1]}"
                            sugestoes.append({
                                'nome': cidade_estado,
                                'endereco_completo': loc.address,
                                'latitude': loc.latitude,
                                'longitude': loc.longitude
                            })
            
            # Armazenar no cache
            self.cache_sugestoes[chave_cache] = {
                'sugestoes': sugestoes,
                'timestamp': time.time()
            }
            
            return sugestoes
            
        except Exception as e:
            print(f"Erro ao buscar sugestões para {termo}: {e}")
            return []
    
    async def obter_latitude_longitude(self, cidade: str) -> tuple[Optional[float], Optional[float]]:
        """Obtém latitude e longitude de uma cidade"""
        try:
            # Normalizar formato da cidade (vírgula e pipe para espaço)
            cidade_normalizada = cidade.replace(',', ' ').replace('|', ' ').strip()
            
            # Verificar cache de coordenadas (válido por 7 dias)
            chave_cache = self.gerar_chave_cache(cidade_normalizada)
            if chave_cache in self.cache_coordenadas:
                dados_cache = self.cache_coordenadas[chave_cache]
                if not self.cache_expirado(dados_cache['timestamp'], 168):  # 7 dias = 168 horas
                    print(f"Cache hit para coordenadas: {cidade_normalizada}")
                    return dados_cache['latitude'], dados_cache['longitude']
                else:
                    del self.cache_coordenadas[chave_cache]
            
            # Dicionário com coordenadas conhecidas para cidades problemáticas
            cidades_conhecidas = {
                'recife pe': (-8.0584933, -34.8848193),
                'recife': (-8.0584933, -34.8848193),
                'jaboatao dos guararapes pe': (-8.1752476, -34.9468716),
                'jaboatão dos guararapes pe': (-8.1752476, -34.9468716),
                'jaboatão dos guararapes': (-8.1752476, -34.9468716),
                'jaboatao dos guararapes': (-8.1752476, -34.9468716),
                'sao paulo sp': (-23.5505, -46.6333),
                'são paulo sp': (-23.5505, -46.6333),
                'sao paulo': (-23.5505, -46.6333),
                'são paulo': (-23.5505, -46.6333),
                'guarulhos sp': (-23.4538, -46.5331),
                'guarulhos': (-23.4538, -46.5331),
                'rio de janeiro rj': (-22.9068, -43.1729),
                'rio de janeiro': (-22.9068, -43.1729),
                'belo horizonte mg': (-19.9167, -43.9345),
                'belo horizonte': (-19.9167, -43.9345),
                'brasilia df': (-15.7801, -47.9292),
                'brasília df': (-15.7801, -47.9292),
                'brasilia': (-15.7801, -47.9292),
                'brasília': (-15.7801, -47.9292),
                'jundiai sp': (-23.1864, -46.8842),
                'jundiaí sp': (-23.1864, -46.8842),
                'jundiai': (-23.1864, -46.8842),
                'jundiaí': (-23.1864, -46.8842),
                # Adicionando mais cidades comuns
                'santos sp': (-23.9608, -46.3331),
                'santos': (-23.9608, -46.3331),
                'campinas sp': (-22.9056, -47.0608),
                'campinas': (-22.9056, -47.0608),
                'sao bernardo do campo sp': (-23.6939, -46.5650),
                'são bernardo do campo sp': (-23.6939, -46.5650),
                'sao bernardo do campo': (-23.6939, -46.5650),
                'são bernardo do campo': (-23.6939, -46.5650),
                'santo andre sp': (-23.6639, -46.5383),
                'santo andré sp': (-23.6639, -46.5383),
                'santo andre': (-23.6639, -46.5383),
                'santo andré': (-23.6639, -46.5383),
                'osasco sp': (-23.5329, -46.7919),
                'osasco': (-23.5329, -46.7919),
                'sao caetano do sul sp': (-23.6231, -46.5512),
                'são caetano do sul sp': (-23.6231, -46.5512),
                'sao caetano do sul': (-23.6231, -46.5512),
                'são caetano do sul': (-23.6231, -46.5512),
                # Adicionando ATIBAIA SP que estava falhando
                'atibaia sp': (-23.1169, -46.5503),
                'atibaia': (-23.1169, -46.5503)
            }
            
            # Verificar se a cidade está na lista de cidades conhecidas
            cidade_lower = cidade_normalizada.lower().strip()
            print(f"🔍 Buscando coordenadas para: '{cidade}'")
            print(f"🔧 Normalizada: '{cidade_normalizada}'")
            
            # Tentar diferentes variações da cidade normalizada
            variacoes_cidade = [
                cidade_lower,
                cidade_lower.replace('  ', ' '),  # Remove espaços duplos
                cidade_lower.replace(' sp', ' sp').strip(),
                cidade_lower.replace(' pe', ' pe').strip(),
                cidade_lower.replace(' rj', ' rj').strip(),
                cidade_lower.replace(' mg', ' mg').strip(),
                cidade_lower.replace(' pr', ' pr').strip(),
                cidade_lower.replace(' rs', ' rs').strip(),
                cidade_lower.replace(' sc', ' sc').strip(),
                cidade_lower.replace(' ba', ' ba').strip(),
                cidade_lower.replace(' ce', ' ce').strip(),
                cidade_lower.replace(' df', ' df').strip()
            ]
            
            # Remover duplicatas mantendo ordem
            variacoes_cidade = list(dict.fromkeys(variacoes_cidade))
            
            for variacao in variacoes_cidade:
                if variacao in cidades_conhecidas:
                    lat, lon = cidades_conhecidas[variacao]
                    # Armazenar no cache
                    self.cache_coordenadas[chave_cache] = {
                        'latitude': lat,
                        'longitude': lon,
                        'timestamp': time.time()
                    }
                    print(f"✅ Coordenada encontrada no banco de dados: {lat}, {lon}")
                    return lat, lon
            
            print(f"🌐 Buscando coordenadas na API do Nominatim...")
            geolocator = Nominatim(user_agent="calculadora_rotas_v2", timeout=10)
            
            # Busca mais simples e eficiente - como funcionava antes
            search_queries = [
                f"{cidade_normalizada}, Brasil",
                f"{cidade_normalizada}, SP, Brasil",
                f"{cidade_normalizada}, RJ, Brasil", 
                f"{cidade_normalizada}, MG, Brasil",
                f"{cidade_normalizada}, PR, Brasil",
                f"{cidade_normalizada}, RS, Brasil",
                f"{cidade_normalizada}, SC, Brasil",
                f"{cidade_normalizada}, BA, Brasil",
                f"{cidade_normalizada}, CE, Brasil",
                f"{cidade_normalizada}, PE, Brasil"
            ]
            
            location = None
            for i, query in enumerate(search_queries, 1):
                try:
                    print(f"🔍 Tentativa {i}/{len(search_queries)}: {query}")
                    location = geolocator.geocode(query, exactly_one=True)
                    if location and location.address:
                        # Validação mais simples - apenas verificar se contém a cidade
                        cidade_clean = cidade_normalizada.lower().replace(' sp', '').replace('sp', '').replace(' pe', '').replace('pe', '').replace(' rj', '').replace('rj', '').replace(' mg', '').replace('mg', '').replace(' pr', '').replace('pr', '').replace(' rs', '').replace('rs', '').replace(' sc', '').replace('sc', '').replace(' ba', '').replace('ba', '').replace(' ce', '').replace('ce', '').strip()
                        address_lower = location.address.lower()
                        
                        # Verificação mais flexível - se a cidade principal está no endereço
                        cidade_principal = cidade_clean.split()[0] if cidade_clean.split() else cidade_clean
                        if cidade_principal in address_lower and len(cidade_principal) > 2:
                            print(f"✅ Coordenada válida encontrada: {location.address}")
                            break
                        else:
                            print(f"❌ Coordenada rejeitada: {location.address}")
                            location = None
                except Exception as e:
                    print(f"❌ Erro na busca: {e}")
                    continue
            
            if location:
                # Armazenar no cache
                self.cache_coordenadas[chave_cache] = {
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'timestamp': time.time()
                }
                print(f"✅ Coordenada encontrada e salva: {location.latitude}, {location.longitude}")
                print(f"📍 Endereço: {location.address}")
                return location.latitude, location.longitude
            else:
                print(f"❌ Coordenadas não encontradas para: {cidade}")
                return None, None
        except Exception as e:
            print(f"❌ Erro ao obter coordenadas para {cidade}: {e}")
            return None, None
    
    async def criar_string_pontos_por_cidades(self, cidades: List[str]) -> Optional[str]:
        """Cria string de pontos para a API de rotas"""
        print(f"🔗 Criando string de pontos para {len(cidades)} cidades...")
        coordenadas = []
        for i, cidade in enumerate(cidades, 1):
            print(f"📍 Processando cidade {i}/{len(cidades)}: {cidade}")
            latitude, longitude = await self.obter_latitude_longitude(cidade)
            if latitude is not None and longitude is not None:
                coordenadas.append((latitude, longitude))
                print(f"✅ Coordenada adicionada: {latitude}, {longitude}")
            else:
                print(f"❌ Coordenadas não encontradas para: {cidade}")
                return None
        
        if len(coordenadas) < 2:
            print(f"❌ Mínimo de 2 coordenadas necessárias, encontradas: {len(coordenadas)}")
            return None
            
        pontos = ""
        for coordenada in coordenadas:
            pontos += f"{coordenada[1]},{coordenada[0]};"
        pontos_final = pontos[:-1]  # Remove o último ponto e vírgula desnecessários
        print(f"✅ String de pontos criada: {pontos_final}")
        return pontos_final
    
    async def chamar_api_rotas_brasil(self, url: str) -> Dict[str, Any]:
        """Chama a API do Rotas Brasil"""
        try:
            print(f"🌐 Fazendo requisição para API do Rotas Brasil...")
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
            print(f"✅ Resposta recebida da API (status: {response.status_code})")
            return response.json()
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout na API - tente novamente")
            raise Exception("Timeout na API - tente novamente")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {str(e)}")
            raise Exception(f"Erro na requisição: {str(e)}")
        except json.JSONDecodeError:
            print(f"❌ Resposta inválida da API")
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
            return 0
    
    async def processar_rota(self, origem: str, destino: str) -> Dict[str, Any]:
        """Processa uma rota individual - FUNÇÃO PRINCIPAL REUTILIZADA"""
        try:
            print(f"\n🚀 === NOVA ROTA RECEBIDA ===")
            print(f"📍 Origem: {origem}")
            print(f"📍 Destino: {destino}")
            
            # Verificar cache de rotas (válido por 6 horas)
            chave_rota = self.gerar_chave_cache(f"{origem}->{destino}")
            if chave_rota in self.cache_rotas:
                dados_cache = self.cache_rotas[chave_rota]
                if not self.cache_expirado(dados_cache['timestamp'], 6):  # 6 horas
                    print(f"💾 Cache encontrado - retornando dados salvos")
                    return dados_cache['resultado']
                else:
                    print(f"⏰ Cache expirado - removendo")
                    del self.cache_rotas[chave_rota]
            
            print(f"🔍 Buscando coordenadas das cidades...")
            # Calcula distância e pedágios
            lista_cidades = [origem, destino]
            pontos_formatados = await self.criar_string_pontos_por_cidades(lista_cidades)
            
            if not pontos_formatados:
                print(f"❌ Erro: Cidades não encontradas")
                resultado = {
                    "origem": origem,
                    "destino": destino,
                    "distance": 0,
                    "pedagios": 0
                }
                return resultado
            
            print(f"✅ Coordenadas encontradas: {pontos_formatados}")
            
            print(f"🌐 Chamando API do Rotas Brasil...")
            url_ajustada = f'{settings.rotas_brasil_api_url}?pontos={pontos_formatados}&alternatives=true&eixos=2&veiculo=1&st=false&combustivel=&consumo=&evitarPedagio=false&recaptchaRespostaCliente=03AFcWeA7j9naH_X1GiW2hXsNijAAl6OD4BGA4Ivh1_OyCx6W_v0z9EU26aLcc5pBUAh7-4RtMF16tD2fXZD-2A2pjC5DkhCEjsvhAnAss5WiYyTJbVc9_s-ggLNMRBIEWu8ZQW1AfHPqCSbKXkQ4XZhCxFgAzYzmF8udZAfhNEI7T6L6Jvcc6vF2ONx-ax9pIJAxmTz3OAFjy4dWCaGCMD9qwb17Fmxm44JP7EiCHm3lRdd_RGGWLQpUagh5gRix6x2U6R0CPffZ1uBpOv3oeM1pSjz0Eoutl_9HUB0nVJQNHIj7huLHV7wpIVj0B2VY5LvuHhh94ysYnWLu9-IqhLihEgOIVlgfjoCae5p0Yl2cUcmwHyyakjjbKpavnD2jfbkPFA97YQ2wcLBOFV6OqtkZ-dceO1yMIo1pp-PEXH7gz2j0QIFB-c8H158UzpacH-27tf8N1Ithk-88ckLZM3U2a1uAgQUhxYDm4Db3ZRFvyT_wydTfFZBGPgSTV1f2-ahy88wEhzxjPkeY7nTo1UNMZcrjnmiau9g--83jPyQSvlUi31MwUobR8AIHRkysOqMctf6WGtwZl9zSCPfurXU-9f95OTK9BZMnTxHpLl_G_7JwZAVc4bdDwh5BSGxPRKnBbeFdaus462FQckgFrtH3aH6Bb4fA_wBIKa5umFMy3xSbXhIXmumPpzUCtXLEyEl30cbrdConCE9_BvoMXwsXqD52bRqONT7rH_KzthaTT0DgE1Eb9x5U&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29'
            
            resposta = await self.chamar_api_rotas_brasil(url_ajustada)
            
            # Validação da resposta
            if not resposta or 'routes' not in resposta or not resposta['routes']:
                print(f"❌ Erro: Rota não encontrada na API")
                resultado = {
                    "origem": origem,
                    "destino": destino,
                    "distance": 0,
                    "pedagios": 0
                }
                return resultado
            
            print(f"✅ Resposta da API recebida com sucesso")
            
            route = resposta['routes'][0]
            
            if 'distance' not in route:
                print(f"❌ Erro: Distância não disponível na resposta")
                resultado = {
                    "origem": origem,
                    "destino": destino,
                    "distance": 0,
                    "pedagios": 0
                }
                return resultado
            
            print(f"📏 Processando distância...")
            distance = (route['distance'] / 1000)
            distance = round(distance, 2)
            print(f"📏 Distância calculada: {distance} km")
            
            # Tratamento de pedágios
            print(f"💰 Calculando pedágios...")
            preco_pedagio = 0
            if 'pedagios' in route and route['pedagios']:
                try:
                    preco_pedagio = await self.calcular_pedagio(route['pedagios'])
                    preco_pedagio = round(preco_pedagio, 2)
                    print(f"💰 Pedágios calculados: R$ {preco_pedagio}")
                except Exception as e:
                    print(f"❌ Erro ao calcular pedágios: {e}")
                    preco_pedagio = 0
            else:
                print(f"💰 Nenhum pedágio encontrado")
            
            resultado = {
                "origem": origem,
                "destino": destino,
                "distance": distance,
                "pedagios": preco_pedagio
            }
            
            # Armazenar no cache com validação adicional
            self.cache_rotas[chave_rota] = {
                'resultado': resultado,
                'timestamp': time.time(),
                'validado': True  # Flag para indicar que foi validado
            }
            
            print(f"💾 Resultado salvo no cache")
            print(f"🎯 === RESULTADO FINAL ===")
            print(f"📍 {origem} → {destino}")
            print(f"📏 Distância: {distance} km")
            print(f"💰 Pedágios: R$ {preco_pedagio}")
            print(f"✅ Rota processada com sucesso!\n")
            return resultado
            
        except Exception as e:
            print(f"Erro ao processar rota {origem} -> {destino}: {e}")
            return {
                "origem": origem,
                "destino": destino,
                "distance": 0,
                "pedagios": 0
            }
    
    async def processar_rota_multipla(self, origem: str, destinos_lista: List[str]) -> Dict[str, Any]:
        """Processa uma rota com múltiplos destinos em sequência - FUNÇÃO PRINCIPAL REUTILIZADA"""
        try:
            # Verificar cache de rotas múltiplas
            destinos_str = ", ".join(destinos_lista)
            chave_rota = self.gerar_chave_cache(f"{origem}->{destinos_str}")
            if chave_rota in self.cache_rotas:
                dados_cache = self.cache_rotas[chave_rota]
                if not self.cache_expirado(dados_cache['timestamp'], 6):  # 6 horas
                    print(f"Cache hit para rota múltipla: {origem} -> {destinos_str}")
                    return dados_cache['resultado']
                else:
                    del self.cache_rotas[chave_rota]
            
            # Criar lista completa da rota: origem + todos os destinos
            rota_completa = [origem] + destinos_lista
            
            # Calcular rota completa
            pontos_formatados = await self.criar_string_pontos_por_cidades(rota_completa)
            
            if not pontos_formatados:
                resultado = {
                    "origem": origem,
                    "destino": destinos_str,
                    "distance": 0,
                    "pedagios": 0
                }
                return resultado
            
            url_ajustada = f'{settings.rotas_brasil_api_url}?pontos={pontos_formatados}&alternatives=true&eixos=2&veiculo=1&st=false&combustivel=&consumo=&evitarPedagio=false&recaptchaRespostaCliente=03AFcWeA7j9naH_X1GiW2hXsNijAAl6OD4BGA4Ivh1_OyCx6W_v0z9EU26aLcc5pBUAh7-4RtMF16tD2fXZD-2A2pjC5DkhCEjsvhAnAss5WiYyTJbVc9_s-ggLNMRBIEWu8ZQW1AfHPqCSbKXkQ4XZhCxFgAzYzmF8udZAfhNEI7T6L6Jvcc6vF2ONx-ax9pIJAxmTz3OAFjy4dWCaGCMD9qwb17Fmxm44JP7EiCHm3lRdd_RGGWLQpUagh5gRix6x2U6R0CPffZ1uBpOv3oeM1pSjz0Eoutl_9HUB0nVJQNHIj7huLHV7wpIVj0B2VY5LvuHhh94ysYnWLu9-IqhLihEgOIVlgfjoCae5p0Yl2cUcmwHyyakjjbKpavnD2jfbkPFA97YQ2wcLBOFV6OqtkZ-dceO1yMIo1pp-PEXH7gz2j0QIFB-c8H158UzpacH-27tf8N1Ithk-88ckLZM3U2a1uAgQUhxYDm4Db3ZRFvyT_wydTfFZBGPgSTV1f2-ahy88wEhzxjPkeY7nTo1UNMZcrjnmiau9g--83jPyQSvlUi31MwUobR8AIHRkysOqMctf6WGtwZl9zSCPfurXU-9f95OTK9BZMnTxHpLl_G_7JwZAVc4bdDwh5BSGxPRKnBbeFdaus462FQckgFrtH3aH6Bb4fA_wBIKa5umFMy3xSbXhIXmumPpzUCtXLEyEl30cbrdConCE9_BvoMXwsXqD52bRqONT7rH_KzthaTT0DgE1Eb9x5U&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29'
            
            resposta = await self.chamar_api_rotas_brasil(url_ajustada)
            
            # Validação da resposta
            if not resposta or 'routes' not in resposta or not resposta['routes']:
                resultado = {
                    "origem": origem,
                    "destino": destinos_str,
                    "distance": 0,
                    "pedagios": 0
                }
                return resultado
            
            route = resposta['routes'][0]
            
            if 'distance' not in route:
                resultado = {
                    "origem": origem,
                    "destino": destinos_str,
                    "distance": 0,
                    "pedagios": 0
                }
                return resultado
            
            distance = (route['distance'] / 1000)
            distance = round(distance, 2)
            
            # Tratamento de pedágios
            preco_pedagio = 0
            if 'pedagios' in route and route['pedagios']:
                try:
                    preco_pedagio = await self.calcular_pedagio(route['pedagios'])
                    preco_pedagio = round(preco_pedagio, 2)
                except Exception as e:
                    print(f"Erro ao calcular pedágios: {e}")
                    preco_pedagio = 0
            
            resultado = {
                "origem": origem,
                "destino": destinos_str,
                "distance": distance,
                "pedagios": preco_pedagio
            }
            
            # Armazenar no cache com validação adicional
            self.cache_rotas[chave_rota] = {
                'resultado': resultado,
                'timestamp': time.time(),
                'validado': True  # Flag para indicar que foi validado
            }
            
            print(f"Rota múltipla processada e cacheada: {origem} -> {' -> '.join(destinos_lista)}")
            return resultado
            
        except Exception as e:
            print(f"Erro ao processar rota múltipla {origem} -> {destinos_lista}: {e}")
            return {
                "origem": origem,
                "destino": ", ".join(destinos_lista),
                "distance": 0,  # Retornar 0 em vez de string de erro
                "pedagios": 0   # Retornar 0 em vez de string de erro
            }
    
    async def processar_rota_com_cache(self, origem: str, destino: str, 
                                     planilha_id: str = None, grupo_id: int = None, 
                                     ip_address: str = None, db = None, 
                                     usar_cache: bool = True) -> Dict[str, Any]:
        """
        Processa uma rota com sistema de cache inteligente
        """
        try:
            # 1. Verificar se deve usar cache e se existe no cache
            if usar_cache:
                cache_result = cache_service.buscar_no_cache(origem, destino, db)
                if cache_result:
                    # Salvar consulta marcando como cache hit
                    consulta = Consulta(
                        planilha_id=planilha_id,
                        origem=origem,
                        destino=destino,
                        distancia=cache_result["distancia"],
                        pedagios=cache_result["pedagios"],
                        ip_address=ip_address,
                        tipo_consulta="batch",
                        grupo_id=grupo_id,
                        cache_hit="true"
                    )
                    db.add(consulta)
                    db.commit()
                    
                    return {
                        "origem": origem,
                        "destino": destino,
                        "distance": cache_result["distancia"],
                        "pedagios": cache_result["pedagios"],
                        "fonte": "cache"
                    }
            
            # 2. Se não encontrou no cache ou não quer usar cache, calcular via API
            print(f"🔄 Calculando via API: {origem} → {destino}")
            resultado = await self.processar_rota(origem, destino)
            
            # 3. Salvar no cache para futuras consultas
            # Verificar se o resultado é válido (não é string de erro)
            distancia_valida = isinstance(resultado.get("distance"), (int, float)) and resultado.get("distance", 0) > 0
            pedagios_validos = isinstance(resultado.get("pedagios"), (int, float)) and resultado.get("pedagios", 0) >= 0
            
            if distancia_valida and pedagios_validos:
                cache_service.salvar_no_cache(
                    origem=origem,
                    destino=destino,
                    distancia=float(resultado["distance"]),
                    pedagios=float(resultado["pedagios"]),
                    planilha_id=planilha_id,
                    grupo_id=grupo_id,
                    ip_address=ip_address,
                    db=db
                )
                print(f"💾 Salvo no cache: {origem} → {destino} ({resultado['distance']}km, R${resultado['pedagios']})")
            else:
                print(f"⚠️ Resultado inválido, não salvo no cache: {origem} → {destino} (dist: {resultado.get('distance')}, ped: {resultado.get('pedagios')})")
            
            resultado["fonte"] = "api"
            return resultado
            
        except Exception as e:
            print(f"❌ Erro ao processar rota com cache: {str(e)}")
            return {
                "origem": origem,
                "destino": destino,
                "distance": 0,
                "pedagios": 0,
                "fonte": "erro"
            }
