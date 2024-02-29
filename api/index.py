from flask import Flask

app = Flask(__name__)

from geopy.geocoders import Nominatim

def criar_string_pontos_por_cidades(cidades):
    coordenadas = []
    for cidade in cidades:
        latitude, longitude = obter_latitude_longitude(cidade)
        if latitude is not None and longitude is not None:
            coordenadas.append((latitude, longitude))
    pontos = ""
    for coordenada in coordenadas:
        pontos += f"{coordenada[1]},{coordenada[0]};"
    return pontos[:-1]  # Remove o último ponto e vírgula desnecessários

def chamar_api_rotas_brasil(url):
    headers = {
        'authority': 'rotasbrasil.com.br',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.7',
        'cookie': 'RBNOTIFICATION=true; RBCOUNTNOTIFICATION=19; JSESSIONID=DD991B79A608CF2F40C3DDD0428DD789; veiculo=1; eixo=2; precoCombustivel=; consumo=',
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
    response = requests.get(url, headers=headers)
    return response.text

@app.route('/')
def home():
    

    cidades = ["Jundiai", "Florianopolis", "curitiba"]
    pontos_formatados = criar_string_pontos_por_cidades(cidades)

    url_ajustada = 'https://rotasbrasil.com.br/roterizador/buscaRota/?pontos=' + pontos_formatados +'&alternatives=true&eixos=2&veiculo=1&st=false&combustivel=&consumo=&evitarPedagio=false&recaptchaRespostaCliente=03AFcWeA7j9naH_X1GiW2hXsNijAAl6OD4BGA4Ivh1_OyCx6W_v0z9EU26aLcc5pBUAh7-4RtMF16tD2fXZD-2A2pjC5DkhCEjsvhAnAss5WiYyTJbVc9_s-ggLNMRBIEWu8ZQW1AfHPqCSbKXkQ4XZhCxFgAzYzmF8udZAfhNEI7T6L6Jvcc6vF2ONx-ax9pIJAxmTz3OAFjy4dWCaGCMD9qwb17Fmxm44JP7EiCHm3lRdd_RGGWLQpUagh5gRix6x2U6R0CPffZ1uBpOv3oeM1pSjz0Eoutl_9HUB0nVJQNHIj7huLHV7wpIVj0B2VY5LvuHhh94ysYnWLu9-IqhLihEgOIVlgfjoCae5p0Yl2cUcmwHyyakjjbKpavnD2jfbkPPA97YQ2wcLBOFV6OqtkZ-dceO1yMIo1pp-PEXH7gz2j0QIFB-c8H158UzpacH-27tf8N1Ithk-88ckLZM3U2a1uAgQUhxYDm4Db3ZRFvyT_wydTfFZBGPgSTV1f2-ahy88wEhzxjPkeY7nTo1UNMZcrjnmiau9g--83jPyQSvlUi31MwUobR8AIHRkysOqMctf6WGtwZl9zSCPfurXU-9f95OTK9BZMnTxHpLl_G_7JwZAVc4bdDwh5BSGxPRKnBbeFdaus462FQckgFrtH3aH6Bb4fA_wBIKa5umFMy3xSbXhIXmumPpzUCtXLEyEl30cbrdConCE9_BvoMXwsXqD52bRqONT7rH_KzthaTT0DgE1Eb9x5U&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29' \

    chamar_api_rotas_brasil(url_ajustada)
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'