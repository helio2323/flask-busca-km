import asyncio
from quart import Quart, jsonify, request, render_template
import pandas as pd
import io
import json
import hashlib
import time

app = Quart(__name__)

import requests

from geopy.geocoders import Nominatim

# Sistema de Cache
cache_coordenadas = {}
cache_rotas = {}

def gerar_chave_cache(texto):
    """Gera uma chave única para o cache usando hash MD5"""
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

def cache_expirado(timestamp, duracao_horas):
    """Verifica se o cache expirou"""
    return time.time() - timestamp > (duracao_horas * 3600)

async def obter_latitude_longitude(cidade):
    try:
        # Verificar cache de coordenadas (válido por 7 dias)
        chave_cache = gerar_chave_cache(cidade)
        if chave_cache in cache_coordenadas:
            dados_cache = cache_coordenadas[chave_cache]
            if not cache_expirado(dados_cache['timestamp'], 168):  # 7 dias = 168 horas
                print(f"Cache hit para coordenadas: {cidade}")
                return dados_cache['latitude'], dados_cache['longitude']
            else:
                del cache_coordenadas[chave_cache]
        
        geolocator = Nominatim(user_agent="calculadora_rotas_v2")
        location = geolocator.geocode(cidade + ", Brasil")
        if location:
            # Armazenar no cache
            cache_coordenadas[chave_cache] = {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'timestamp': time.time()
            }
            print(f"Nova coordenada processada e cacheada: {cidade}")
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Erro ao obter coordenadas para {cidade}: {e}")
        return None, None

async def criar_string_pontos_por_cidades(cidades):
    coordenadas = []
    for cidade in cidades:
        latitude, longitude = await obter_latitude_longitude(cidade)
        if latitude is not None and longitude is not None:
            coordenadas.append((latitude, longitude))
        else:
            print(f"Coordenadas não encontradas para: {cidade}")
            return None
    
    if len(coordenadas) < 2:
        return None
        
    pontos = ""
    for coordenada in coordenadas:
        pontos += f"{coordenada[1]},{coordenada[0]};"
    return pontos[:-1]  # Remove o último ponto e vírgula desnecessários

async def chamar_api_rotas_brasil(url):
    try:
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
        return response.json()
    except requests.exceptions.Timeout:
        raise Exception("Timeout na API - tente novamente")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro na requisição: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Resposta inválida da API")

async def calcular_pedagio(loads):
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

async def processar_rota(origem, destino):
    """Processa uma rota individual"""
    try:
        # Verificar cache de rotas (válido por 6 horas)
        chave_rota = gerar_chave_cache(f"{origem}->{destino}")
        if chave_rota in cache_rotas:
            dados_cache = cache_rotas[chave_rota]
            if not cache_expirado(dados_cache['timestamp'], 6):  # 6 horas
                print(f"Cache hit para {origem} -> {destino}")
                return dados_cache['resultado']
            else:
                del cache_rotas[chave_rota]
        
        # Calcula distância e pedágios
        lista_cidades = [origem, destino]
        pontos_formatados = await criar_string_pontos_por_cidades(lista_cidades)
        
        if not pontos_formatados:
            resultado = {
                "origem": origem,
                "destino": destino,
                "distance": "Erro - Cidade não encontrada",
                "pedagios": "Erro - Cidade não encontrada"
            }
            return resultado
        
        url_ajustada = 'https://rotasbrasil.com.br/roterizador/buscaRota/?pontos=' + pontos_formatados +'&alternatives=true&eixos=2&veiculo=1&st=false&combustivel=&consumo=&evitarPedagio=false&recaptchaRespostaCliente=03AFcWeA7j9naH_X1GiW2hXsNijAAl6OD4BGA4Ivh1_OyCx6W_v0z9EU26aLcc5pBUAh7-4RtMF16tD2fXZD-2A2pjC5DkhCEjsvhAnAss5WiYyTJbVc9_s-ggLNMRBIEWu8ZQW1AfHPqCSbKXkQ4XZhCxFgAzYzmF8udZAfhNEI7T6L6Jvcc6vF2ONx-ax9pIJAxmTz3OAFjy4dWCaGCMD9qwb17Fmxm44JP7EiCHm3lRdd_RGGWLQpUagh5gRix6x2U6R0CPffZ1uBpOv3oeM1pSjz0Eoutl_9HUB0nVJQNHIj7huLHV7wpIVj0B2VY5LvuHhh94ysYnWLu9-IqhLihEgOIVlgfjoCae5p0Yl2cUcmwHyyakjjbKpavnD2jfbkPFA97YQ2wcLBOFV6OqtkZ-dceO1yMIo1pp-PEXH7gz2j0QIFB-c8H158UzpacH-27tf8N1Ithk-88ckLZM3U2a1uAgQUhxYDm4Db3ZRFvyT_wydTfFZBGPgSTV1f2-ahy88wEhzxjPkeY7nTo1UNMZcrjnmiau9g--83jPyQSvlUi31MwUobR8AIHRkysOqMctf6WGtwZl9zSCPfurXU-9f95OTK9BZMnTxHpLl_G_7JwZAVc4bdDwh5BSGxPRKnBbeFdaus462FQckgFrtH3aH6Bb4fA_wBIKa5umFMy3xSbXhIXmumPpzUCtXLEyEl30cbrdConCE9_BvoMXwsXqD52bRqONT7rH_KzthaTT0DgE1Eb9x5U&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29'
        
        resposta = await chamar_api_rotas_brasil(url_ajustada)
        
        # Validação da resposta
        if not resposta or 'routes' not in resposta or not resposta['routes']:
            resultado = {
                "origem": origem,
                "destino": destino,
                "distance": "Erro - Rota não encontrada",
                "pedagios": "Erro - Rota não encontrada"
            }
            return resultado
        
        route = resposta['routes'][0]
        
        if 'distance' not in route:
            resultado = {
                "origem": origem,
                "destino": destino,
                "distance": "Erro - Distância não disponível",
                "pedagios": "Erro - Distância não disponível"
            }
            return resultado
        
        distance = (route['distance'] / 1000)
        distance = round(distance, 2)
        
        # Tratamento de pedágios
        preco_pedagio = 0
        if 'pedagios' in route and route['pedagios']:
            try:
                preco_pedagio = await calcular_pedagio(route['pedagios'])
                preco_pedagio = round(preco_pedagio, 2)
            except Exception as e:
                print(f"Erro ao calcular pedágios: {e}")
                preco_pedagio = 0
        
        resultado = {
            "origem": origem,
            "destino": destino,
            "distance": distance,
            "pedagios": preco_pedagio
        }
        
        # Armazenar no cache
        cache_rotas[chave_rota] = {
            'resultado': resultado,
            'timestamp': time.time()
        }
        
        print(f"Nova busca processada e cacheada: {origem} -> {destino}")
        return resultado
        
    except Exception as e:
        print(f"Erro ao processar rota {origem} -> {destino}: {e}")
        return {
            "origem": origem,
            "destino": destino,
            "distance": f"Erro: {str(e)}",
            "pedagios": f"Erro: {str(e)}"
        }

async def processar_rota_multipla(origem, destinos_lista):
    """Processa uma rota com múltiplos destinos em sequência"""
    try:
        # Verificar cache de rotas múltiplas
        destinos_str = ", ".join(destinos_lista)
        chave_rota = gerar_chave_cache(f"{origem}->{destinos_str}")
        if chave_rota in cache_rotas:
            dados_cache = cache_rotas[chave_rota]
            if not cache_expirado(dados_cache['timestamp'], 6):  # 6 horas
                print(f"Cache hit para rota múltipla: {origem} -> {destinos_str}")
                return dados_cache['resultado']
            else:
                del cache_rotas[chave_rota]
        
        # Criar lista completa da rota: origem + todos os destinos
        rota_completa = [origem] + destinos_lista
        
        # Calcular rota completa
        pontos_formatados = await criar_string_pontos_por_cidades(rota_completa)
        
        if not pontos_formatados:
            resultado = {
                "origem": origem,
                "destino": destinos_str,
                "distance": "Erro - Cidade não encontrada",
                "pedagios": "Erro - Cidade não encontrada"
            }
            return resultado
        
        url_ajustada = 'https://rotasbrasil.com.br/roterizador/buscaRota/?pontos=' + pontos_formatados +'&alternatives=true&eixos=2&veiculo=1&st=false&combustivel=&consumo=&evitarPedagio=false&recaptchaRespostaCliente=03AFcWeA7j9naH_X1GiW2hXsNijAAl6OD4BGA4Ivh1_OyCx6W_v0z9EU26aLcc5pBUAh7-4RtMF16tD2fXZD-2A2pjC5DkhCEjsvhAnAss5WiYyTJbVc9_s-ggLNMRBIEWu8ZQW1AfHPqCSbKXkQ4XZhCxFgAzYzmF8udZAfhNEI7T6L6Jvcc6vF2ONx-ax9pIJAxmTz3OAFjy4dWCaGCMD9qwb17Fmxm44JP7EiCHm3lRdd_RGGWLQpUagh5gRix6x2U6R0CPffZ1uBpOv3oeM1pSjz0Eoutl_9HUB0nVJQNHIj7huLHV7wpIVj0B2VY5LvuHhh94ysYnWLu9-IqhLihEgOIVlgfjoCae5p0Yl2cUcmwHyyakjjbKpavnD2jfbkPFA97YQ2wcLBOFV6OqtkZ-dceO1yMIo1pp-PEXH7gz2j0QIFB-c8H158UzpacH-27tf8N1Ithk-88ckLZM3U2a1uAgQUhxYDm4Db3ZRFvyT_wydTfFZBGPgSTV1f2-ahy88wEhzxjPkeY7nTo1UNMZcrjnmiau9g--83jPyQSvlUi31MwUobR8AIHRkysOqMctf6WGtwZl9zSCPfurXU-9f95OTK9BZMnTxHpLl_G_7JwZAVc4bdDwh5BSGxPRKnBbeFdaus462FQckgFrtH3aH6Bb4fA_wBIKa5umFMy3xSbXhIXmumPpzUCtXLEyEl30cbrdConCE9_BvoMXwsXqD52bRqONT7rH_KzthaTT0DgE1Eb9x5U&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29'
        
        resposta = await chamar_api_rotas_brasil(url_ajustada)
        
        # Validação da resposta
        if not resposta or 'routes' not in resposta or not resposta['routes']:
            resultado = {
                "origem": origem,
                "destino": destinos_str,
                "distance": "Erro - Rota não encontrada",
                "pedagios": "Erro - Rota não encontrada"
            }
            return resultado
        
        route = resposta['routes'][0]
        
        if 'distance' not in route:
            resultado = {
                "origem": origem,
                "destino": destinos_str,
                "distance": "Erro - Distância não disponível",
                "pedagios": "Erro - Distância não disponível"
            }
            return resultado
        
        distance = (route['distance'] / 1000)
        distance = round(distance, 2)
        
        # Tratamento de pedágios
        preco_pedagio = 0
        if 'pedagios' in route and route['pedagios']:
            try:
                preco_pedagio = await calcular_pedagio(route['pedagios'])
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
        
        # Armazenar no cache
        cache_rotas[chave_rota] = {
            'resultado': resultado,
            'timestamp': time.time()
        }
        
        print(f"Rota múltipla processada e cacheada: {origem} -> {' -> '.join(destinos_lista)}")
        return resultado
        
    except Exception as e:
        print(f"Erro ao processar rota múltipla {origem} -> {destinos_lista}: {e}")
        return {
            "origem": origem,
            "destino": ", ".join(destinos_lista),
            "distance": f"Erro: {str(e)}",
            "pedagios": f"Erro: {str(e)}"
        }

@app.route('/', methods=['GET'])
async def index():
    return await render_template('index.html')

@app.route('/upload', methods=['POST'])
async def upload_excel():
    files = await request.files
    
    if 'excel_file' not in files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = files['excel_file']
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Arquivo deve ser Excel (.xlsx ou .xls)'}), 400
    
    try:
        # Lê o arquivo Excel
        file_content = file.read()
        df = pd.read_excel(io.BytesIO(file_content))
        
        # Verifica se as colunas necessárias existem
        required_columns = ['origem', 'destino']
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': 'Planilha deve conter colunas: origem, destino'}), 400
        
        resultados = []
        
        for index, row in df.iterrows():
            origem = str(row['origem']).strip()
            destinos_str = str(row['destino']).strip()
            
            if pd.isna(row['origem']) or pd.isna(row['destino']):
                continue
            
            # Separar múltiplos destinos por vírgula
            destinos = [d.strip() for d in destinos_str.split(',') if d.strip()]
            
            # Se há apenas um destino, usar função original
            if len(destinos) == 1:
                resultado = await processar_rota(origem, destinos[0])
            else:
                # Se há múltiplos destinos, processar como rota sequencial
                resultado = await processar_rota_multipla(origem, destinos)
            
            resultados.append(resultado)
        
        return jsonify({"resultados": resultados})
        
    except Exception as e:
        print(f"Erro geral no upload: {e}")
        return jsonify({'error': f'Erro ao processar arquivo: {str(e)}'}), 500

@app.route('/calculate_route', methods=['POST'])
async def calculate_route():
    """Calcula uma rota individual"""
    try:
        data = await request.get_json()
        
        if not data or 'origem' not in data or 'destino' not in data:
            return jsonify({'error': 'Origem e destino são obrigatórios'}), 400
        
        origem = str(data['origem']).strip()
        destino = str(data['destino']).strip()
        
        if not origem or not destino:
            return jsonify({'error': 'Origem e destino não podem estar vazios'}), 400
        
        # Processar a rota
        resultado = await processar_rota(origem, destino)
        
        # Retornar apenas distância e pedágios
        return jsonify({
            "distance": resultado["distance"],
            "pedagios": resultado["pedagios"]
        })
        
    except Exception as e:
        print(f"Erro ao calcular rota individual: {e}")
        return jsonify({'error': f'Erro ao calcular rota: {str(e)}'}), 500

@app.route('/km/<path:cidades>', methods=['GET'])
async def home(cidades):
    lista_cidades = cidades.split("/")
    
    if len(lista_cidades) < 2:
        return jsonify({"error": "Pelo menos duas cidades são necessárias"}), 400
    
    origem = lista_cidades[0]
    destino = lista_cidades[1]
    
    resultado = await processar_rota(origem, destino)
    
    # Remove campos de origem e destino para manter compatibilidade com API original
    return jsonify({
        "distance": resultado["distance"],
        "pedagios": resultado["pedagios"]
    })

@app.route('/cache/stats', methods=['GET'])
async def cache_stats():
    """Retorna estatísticas do cache"""
    # Limpar caches expirados
    agora = time.time()
    
    # Limpar coordenadas expiradas (7 dias)
    coordenadas_expiradas = [k for k, v in cache_coordenadas.items() 
                           if agora - v['timestamp'] > (168 * 3600)]
    for k in coordenadas_expiradas:
        del cache_coordenadas[k]
    
    # Limpar rotas expiradas (6 horas)
    rotas_expiradas = [k for k, v in cache_rotas.items() 
                      if agora - v['timestamp'] > (6 * 3600)]
    for k in rotas_expiradas:
        del cache_rotas[k]
    
    return jsonify({
        "coordenadas_cache": len(cache_coordenadas),
        "rotas_cache": len(cache_rotas),
        "total_entradas": len(cache_coordenadas) + len(cache_rotas)
    })

@app.route('/cache/clear', methods=['POST'])
async def limpar_cache():
    """Limpa todo o cache"""
    global cache_coordenadas, cache_rotas
    cache_coordenadas.clear()
    cache_rotas.clear()
    return jsonify({"message": "Cache limpo com sucesso"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
