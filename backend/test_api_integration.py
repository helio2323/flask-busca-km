#!/usr/bin/env python3
"""
Script de teste para verificar a integração completa da API com webscraping
"""

import asyncio
import sys
import os

# Adicionar o diretório do backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.route_service import RouteService

async def test_api_integration():
    """Testa a integração completa da API"""
    print("🧪 === TESTE DE INTEGRAÇÃO COMPLETA ===")
    
    # Criar instância do serviço
    route_service = RouteService()
    
    # Teste 1: Rota individual
    print("\n📍 Teste 1: Rota individual via API")
    print("Origem: Sumaré, São Paulo, BR")
    print("Destino: Jundiaí, São Paulo, BR")
    
    try:
        resultado = await route_service.processar_rota(
            "Sumaré, São Paulo, BR",
            "Jundiaí, São Paulo, BR"
        )
        
        print(f"✅ Resultado:")
        print(f"   Distância: {resultado['distance']} km")
        print(f"   Pedágios: R$ {resultado['pedagios']}")
        print(f"   Fonte: {resultado.get('fonte', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Erro no teste 1: {e}")
    
    # Teste 2: Rota múltipla
    print("\n📍 Teste 2: Rota múltipla via API")
    print("Origem: São Paulo, SP, BR")
    print("Destinos: ['Campinas, SP, BR', 'Santos, SP, BR']")
    
    try:
        resultado_multiplo = await route_service.processar_rota_multipla(
            "São Paulo, SP, BR",
            ["Campinas, SP, BR", "Santos, SP, BR"]
        )
        
        print(f"✅ Resultado múltiplo:")
        print(f"   Distância: {resultado_multiplo['distance']} km")
        print(f"   Pedágios: R$ {resultado_multiplo['pedagios']}")
        print(f"   Fonte: {resultado_multiplo.get('fonte', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Erro no teste 2: {e}")
    
    # Teste 3: Cache
    print("\n📍 Teste 3: Verificação de cache")
    print("Repetindo o teste 1 para verificar cache...")
    
    try:
        resultado_cache = await route_service.processar_rota(
            "Sumaré, São Paulo, BR",
            "Jundiaí, São Paulo, BR"
        )
        
        print(f"✅ Resultado (deve vir do cache):")
        print(f"   Distância: {resultado_cache['distance']} km")
        print(f"   Pedágios: R$ {resultado_cache['pedagios']}")
        print(f"   Fonte: {resultado_cache.get('fonte', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Erro no teste 3: {e}")
    
    print("\n🎯 === TESTE DE INTEGRAÇÃO CONCLUÍDO ===")

if __name__ == "__main__":
    print("🚀 Iniciando teste de integração...")
    asyncio.run(test_api_integration())
