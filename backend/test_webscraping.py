#!/usr/bin/env python3
"""
Script de teste para verificar a integração com Selenoid
"""

import asyncio
import sys
import os

# Adicionar o diretório do backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.webscraping_service import WebScrapingService

async def test_webscraping():
    """Testa o webscraping com Selenoid"""
    print("🧪 === TESTE DE WEBSCRAPING COM SELENOID ===")
    
    # Criar instância do serviço
    webscraping_service = WebScrapingService()
    
    # Teste 1: Rota simples
    print("\n📍 Teste 1: Rota simples")
    print("Origem: Sumaré, São Paulo, BR")
    print("Destino: Jundiaí, São Paulo, BR")
    
    try:
        resultado = await webscraping_service.calcular_rota_webscraping(
            "Sumaré, São Paulo, BR",
            "Jundiaí, São Paulo, BR"
        )
        
        print(f"✅ Resultado:")
        print(f"   Distância: {resultado['distance']} km")
        print(f"   Pedágios: R$ {resultado['pedagios']}")
        print(f"   Fonte: {resultado['fonte']}")
        
    except Exception as e:
        print(f"❌ Erro no teste 1: {e}")
    
    # Teste 2: Rota múltipla
    print("\n📍 Teste 2: Rota múltipla")
    print("Origem: São Paulo, SP, BR")
    print("Destinos: ['Campinas, SP, BR', 'Santos, SP, BR']")
    
    try:
        resultado_multiplo = await webscraping_service.calcular_rota_multipla_webscraping(
            "São Paulo, SP, BR",
            ["Campinas, SP, BR", "Santos, SP, BR"]
        )
        
        print(f"✅ Resultado múltiplo:")
        print(f"   Distância: {resultado_multiplo['distance']} km")
        print(f"   Pedágios: R$ {resultado_multiplo['pedagios']}")
        print(f"   Fonte: {resultado_multiplo['fonte']}")
        
    except Exception as e:
        print(f"❌ Erro no teste 2: {e}")
    
    print("\n🎯 === TESTE CONCLUÍDO ===")

async def test_selenoid_connection():
    """Testa apenas a conexão com Selenoid"""
    print("🔌 === TESTE DE CONEXÃO COM SELENOID ===")
    
    webscraping_service = WebScrapingService()
    
    try:
        # Tentar criar driver
        driver = webscraping_service._create_driver()
        print("✅ Driver criado com sucesso!")
        
        # Navegar para o site
        driver.get("https://rotasbrasil.com.br/")
        print("✅ Site carregado com sucesso!")
        
        # Verificar se os elementos estão presentes
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, 10)
        
        # Aguardar elementos principais
        origem_input = wait.until(EC.presence_of_element_located((By.ID, "txtEnderecoPartida")))
        destino_input = wait.until(EC.presence_of_element_located((By.ID, "txtEnderecoChegada")))
        search_button = wait.until(EC.presence_of_element_located((By.ID, "btnSubmit")))
        
        print("✅ Elementos principais encontrados!")
        print(f"   - Campo origem: {origem_input.is_displayed()}")
        print(f"   - Campo destino: {destino_input.is_displayed()}")
        print(f"   - Botão buscar: {search_button.is_displayed()}")
        
        # Fechar driver
        webscraping_service._close_driver()
        print("✅ Driver fechado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        try:
            webscraping_service._close_driver()
        except:
            pass

if __name__ == "__main__":
    print("🚀 Iniciando testes...")
    
    # Teste de conexão primeiro
    asyncio.run(test_selenoid_connection())
    
    # Aguardar um pouco antes do teste completo
    print("\n⏳ Aguardando 3 segundos antes do teste completo...")
    asyncio.run(asyncio.sleep(3))
    
    # Teste completo
    asyncio.run(test_webscraping())
