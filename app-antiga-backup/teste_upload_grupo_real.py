import requests
import pandas as pd
import io

# Dados de teste com as rotas que você mencionou
dados_teste = {
    'origem': ['ARAÇARIGUAMA SP', 'ARAÇARIGUAMA SP', 'GUARULHOS SP'],
    'destino': ['ARAÇATUBA SP', 'ATIBAIA SP', 'JUNDIAI SP']
}

# Criar DataFrame
df = pd.DataFrame(dados_teste)

# Salvar em Excel em memória
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Rotas', index=False)

output.seek(0)

# Fazer upload para o grupo ID 3
url = "http://localhost:8000/api/v1/routes/upload"
files = {'file': ('teste_rotas_aracariguama.xlsx', output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
params = {'grupo_id': 3}

print("🚀 Fazendo upload da planilha ARAÇARIGUAMA para o grupo...")
print(f"📋 Rotas a serem processadas:")
for i, (origem, destino) in enumerate(zip(dados_teste['origem'], dados_teste['destino']), 1):
    print(f"  {i}. {origem} → {destino}")

response = requests.post(url, files=files, params=params)

if response.status_code == 200:
    print("✅ Upload realizado com sucesso!")
    print(f"📊 Resposta: {response.json()}")
else:
    print(f"❌ Erro no upload: {response.status_code}")
    print(f"📝 Detalhes: {response.text}")

# Verificar estatísticas do grupo após upload
print("\n🔍 Verificando estatísticas do grupo...")
grupo_response = requests.get("http://localhost:8000/api/v1/groups/3")
if grupo_response.status_code == 200:
    grupo = grupo_response.json()
    print(f"📊 Grupo: {grupo['nome']}")
    print(f"📈 Total de rotas: {grupo['total_rotas']}")
    print(f"🛣️ Total de distância: {grupo['total_distancia']} km")
    print(f"💰 Total de pedágios: R$ {grupo['total_pedagios']}")
else:
    print(f"❌ Erro ao buscar grupo: {grupo_response.status_code}")

# Verificar rotas do grupo
print("\n🔍 Verificando rotas do grupo...")
rotas_response = requests.get("http://localhost:8000/api/v1/groups/3/rotas")
if rotas_response.status_code == 200:
    rotas = rotas_response.json()
    print(f"📊 Total de rotas no grupo: {rotas['total_rotas']}")
    for i, rota in enumerate(rotas['rotas'], 1):
        print(f"  {i}. {rota['origem']} → {rota['destino']} ({rota['distancia']} km, R$ {rota['pedagios']})")
else:
    print(f"❌ Erro ao buscar rotas: {rotas_response.status_code}")
