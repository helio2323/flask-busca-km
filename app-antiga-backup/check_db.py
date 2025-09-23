import sqlite3

conn = sqlite3.connect('rotas.db')
cursor = conn.cursor()

print('=== TABELAS NO BANCO ===')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = cursor.fetchall()
for tabela in tabelas:
    print(f'Tabela: {tabela[0]}')

print('\n=== CONSULTAS NO BANCO ===')
cursor.execute("SELECT id, origem, destino, distancia, pedagios, data_consulta, grupo_id FROM consulta WHERE grupo_id = 3 ORDER BY data_consulta DESC")
consultas = cursor.fetchall()

for consulta in consultas:
    print(f'ID: {consulta[0]}')
    print(f'Origem: {consulta[1]}')
    print(f'Destino: {consulta[2]}')
    print(f'Distância: {consulta[3]}')
    print(f'Pedágios: {consulta[4]}')
    print(f'Data: {consulta[5]}')
    print(f'Grupo ID: {consulta[6]}')
    print('---')

print('\n=== TODAS AS CONSULTAS RECENTES ===')
cursor.execute("SELECT id, origem, destino, distancia, pedagios, data_consulta, grupo_id FROM consulta ORDER BY data_consulta DESC LIMIT 10")
consultas = cursor.fetchall()

for consulta in consultas:
    print(f'ID: {consulta[0]} | Origem: {consulta[1]} | Destino: {consulta[2]} | Grupo: {consulta[6]} | Data: {consulta[5]}')

conn.close()
