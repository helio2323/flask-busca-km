#!/usr/bin/env python3
"""
Teste simples para verificar configuração do Selenoid
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_selenoid():
    print("🧪 Teste simples do Selenoid")
    
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--enable-vnc")
        chrome_options.add_argument("--screen-resolution=1920x1080x24")
        chrome_options.add_argument("--disable-video")
        
        print("🔧 Configurações do Chrome:")
        for arg in chrome_options.arguments:
            print(f"   - {arg}")
        
        print("\n🌐 Conectando ao Selenoid...")
        
        # Adicionar configurações específicas do Selenoid
        chrome_options.add_argument("--browser-version=127.0")
        
        driver = webdriver.Remote(
            command_executor="http://168.231.89.187:4444/wd/hub",
            options=chrome_options
        )
        
        print("✅ Driver criado com sucesso!")
        
        # Navegar para o site
        driver.get("https://rotasbrasil.com.br/")
        print("✅ Site carregado!")
        
        # Verificar título
        title = driver.title
        print(f"📄 Título da página: {title}")
        
        # Fechar driver
        driver.quit()
        print("✅ Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_selenoid()
