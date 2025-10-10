#!/usr/bin/env python3
import asyncio
import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.rotas_brasil_service import RotasBrasilService

async def test_formato_correto():
    """Testa o formato correto de concatenação"""
    service = RotasBrasilService()
    
    print("=== TESTANDO FORMATO CORRETO ===")
    
    # Testar com formato correto: "Campinas, Sao Paulo, BR"
    print("\n1. Testando formato correto...")
    cidade_completa = await service.buscar_cidade_completa("Campinas, Sao Paulo, BR")
    if cidade_completa:
        print(f"[OK] Cidade encontrada: {cidade_completa['nome_correto']}, {cidade_completa['estado']}")
        print(f"Coordenadas: ({cidade_completa['lat']}, {cidade_completa['lon']})")
    else:
        print("[ERRO] Cidade não encontrada")
    
    # Testar com formato correto: "Adamantina, Sao Paulo, BR"
    print("\n2. Testando Adamantina...")
    cidade_completa = await service.buscar_cidade_completa("Adamantina, Sao Paulo, BR")
    if cidade_completa:
        print(f"[OK] Cidade encontrada: {cidade_completa['nome_correto']}, {cidade_completa['estado']}")
        print(f"Coordenadas: ({cidade_completa['lat']}, {cidade_completa['lon']})")
    else:
        print("[ERRO] Cidade não encontrada")
    
    # Testar processamento de rota completa
    print("\n3. Testando processamento de rota completa...")
    resultado = await service.processar_rota("Campinas, Sao Paulo, BR", "Adamantina, Sao Paulo, BR")
    print(f"Resultado: {resultado}")

if __name__ == "__main__":
    asyncio.run(test_formato_correto())
