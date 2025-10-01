import asyncio
import time
from typing import Optional, Dict, Any, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging

logger = logging.getLogger(__name__)

class WebScrapingService:
    """Serviço de webscraping para rotasbrasil.com.br usando Selenium"""
    
    def __init__(self, selenoid_url: str = "http://168.231.89.187:4444/wd/hub"):
        self.selenoid_url = selenoid_url
        self.driver: Optional[WebDriver] = None
        
    def _create_driver(self) -> WebDriver:
        """Cria e configura o driver do Selenium para Selenoid"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            
            # Configurações para Selenoid
            chrome_options.add_argument("--enable-vnc")
            chrome_options.add_argument("--screen-resolution=1920x1080x24")
            chrome_options.add_argument("--disable-video")
            
            # Especificar versão do Chrome disponível no Selenoid
            chrome_options.add_argument("--browser-version=127.0")
            
            driver = webdriver.Remote(
                command_executor=self.selenoid_url,
                options=chrome_options
            )
            
            # Maximizar janela
            driver.maximize_window()
            
            logger.info("✅ Driver Selenium criado com sucesso")
            return driver
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar driver Selenium: {e}")
            raise
    
    def _close_driver(self):
        """Fecha o driver do Selenium"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                logger.info("✅ Driver Selenium fechado")
        except Exception as e:
            logger.error(f"❌ Erro ao fechar driver: {e}")
    
    async def _wait_for_element(self, by: By, value: str, timeout: int = 10) -> bool:
        """Aguarda elemento aparecer na página"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            logger.warning(f"⏰ Timeout aguardando elemento: {value}")
            return False
    
    async def _fill_origin_destination(self, origem: str, destino: str) -> bool:
        """Preenche origem e destino no site rotasbrasil.com.br"""
        try:
            logger.info(f"📍 Preenchendo origem: {origem}")
            
            # Limpar e preencher origem
            origem_input = self.driver.find_element(By.ID, "txtEnderecoPartida")
            origem_input.clear()
            origem_input.send_keys(origem)
            
            # Aguardar lista de sugestões aparecer
            await asyncio.sleep(1)
            
            # Clicar no primeiro item da lista de sugestões da origem
            try:
                origem_suggestion = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    "ul#ui-id-1 li:first-child div.label-input-autocomplete"
                )
                origem_suggestion.click()
                logger.info("✅ Origem selecionada da lista")
            except NoSuchElementException:
                logger.warning("⚠️ Lista de sugestões da origem não encontrada, continuando...")
            
            logger.info(f"📍 Preenchendo destino: {destino}")
            
            # Limpar e preencher destino
            destino_input = self.driver.find_element(By.ID, "txtEnderecoChegada")
            destino_input.clear()
            destino_input.send_keys(destino)
            
            # Aguardar lista de sugestões aparecer
            await asyncio.sleep(1)
            
            # Clicar no primeiro item da lista de sugestões do destino
            try:
                destino_suggestion = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    "ul#ui-id-2 li:first-child div.label-input-autocomplete"
                )
                destino_suggestion.click()
                logger.info("✅ Destino selecionado da lista")
            except NoSuchElementException:
                logger.warning("⚠️ Lista de sugestões do destino não encontrada, continuando...")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao preencher origem/destino: {e}")
            return False
    
    async def _click_search_button(self) -> bool:
        """Clica no botão de buscar"""
        try:
            search_button = self.driver.find_element(By.ID, "btnSubmit")
            search_button.click()
            logger.info("🔍 Botão de busca clicado")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao clicar no botão de busca: {e}")
            return False
    
    async def _extract_results(self) -> Tuple[Optional[float], Optional[float]]:
        """Extrai KM e pedágio dos resultados"""
        try:
            # Aguardar resultados carregarem
            await asyncio.sleep(6)
            
            # Aguardar elemento de resultado aparecer
            if not await self._wait_for_element(By.CSS_SELECTOR, ".routeResult .distance", timeout=15):
                logger.error("❌ Resultados não carregaram")
                return None, None
            
            # Extrair distância (KM)
            try:
                distance_element = self.driver.find_element(By.CSS_SELECTOR, ".routeResult .distance")
                distance_text = distance_element.text
                # Extrair apenas números da string (ex: "123,45 km" -> 123.45)
                distance_km = float(distance_text.replace(" km", "").replace(",", "."))
                logger.info(f"📏 Distância extraída: {distance_km} km")
            except (NoSuchElementException, ValueError) as e:
                logger.error(f"❌ Erro ao extrair distância: {e}")
                distance_km = None
            
            # Extrair pedágio
            try:
                toll_element = self.driver.find_element(By.CSS_SELECTOR, ".routeResult .vlPedagio")
                toll_text = toll_element.text
                # Extrair apenas números da string (ex: "R$ 45,67" -> 45.67)
                toll_value = float(toll_text.replace("R$", "").replace(",", ".").strip())
                logger.info(f"💰 Pedágio extraído: R$ {toll_value}")
            except (NoSuchElementException, ValueError) as e:
                logger.warning(f"⚠️ Erro ao extrair pedágio: {e}")
                toll_value = 0.0  # Se não encontrar pedágio, assume 0
            
            return distance_km, toll_value
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair resultados: {e}")
            return None, None
    
    async def calcular_rota_webscraping(self, origem: str, destino: str) -> Dict[str, Any]:
        """
        Calcula rota usando webscraping no site rotasbrasil.com.br
        Baseado no código VBA fornecido
        """
        try:
            logger.info(f"🚀 Iniciando webscraping: {origem} → {destino}")
            
            # Criar driver
            self.driver = self._create_driver()
            
            # Navegar para o site
            self.driver.get("https://rotasbrasil.com.br/")
            logger.info("🌐 Site carregado")
            
            # Aguardar página carregar
            await self._wait_for_element(By.ID, "txtEnderecoPartida", timeout=10)
            
            # Preencher origem e destino
            if not await self._fill_origin_destination(origem, destino):
                raise Exception("Erro ao preencher origem/destino")
            
            # Clicar em buscar
            if not await self._click_search_button():
                raise Exception("Erro ao clicar no botão de busca")
            
            # Extrair resultados
            distance, toll = await self._extract_results()
            
            # Preparar resultado
            resultado = {
                "origem": origem,
                "destino": destino,
                "distance": distance if distance is not None else 0,
                "pedagios": toll if toll is not None else 0,
                "fonte": "webscraping"
            }
            
            logger.info(f"✅ Webscraping concluído: {distance}km, R${toll}")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro no webscraping: {e}")
            return {
                "origem": origem,
                "destino": destino,
                "distance": 0,
                "pedagios": 0,
                "fonte": "erro_webscraping"
            }
        finally:
            # Sempre fechar o driver
            self._close_driver()
    
    async def calcular_rota_multipla_webscraping(self, origem: str, destinos: list) -> Dict[str, Any]:
        """
        Calcula rota múltipla usando webscraping
        Para múltiplos destinos, calcula sequencialmente
        """
        try:
            logger.info(f"🚀 Iniciando webscraping múltiplo: {origem} → {destinos}")
            
            total_distance = 0
            total_toll = 0
            destinos_processados = []
            
            # Calcular cada segmento da rota
            pontos_rota = [origem] + destinos
            for i in range(len(pontos_rota) - 1):
                origem_atual = pontos_rota[i]
                destino_atual = pontos_rota[i + 1]
                
                logger.info(f"📍 Calculando segmento {i+1}/{len(pontos_rota)-1}: {origem_atual} → {destino_atual}")
                
                resultado_segmento = await self.calcular_rota_webscraping(origem_atual, destino_atual)
                
                if resultado_segmento["distance"] > 0:
                    total_distance += resultado_segmento["distance"]
                    total_toll += resultado_segmento["pedagios"]
                    destinos_processados.append(destino_atual)
                else:
                    logger.warning(f"⚠️ Falha no segmento: {origem_atual} → {destino_atual}")
            
            resultado = {
                "origem": origem,
                "destino": ", ".join(destinos),
                "distance": round(total_distance, 2),
                "pedagios": round(total_toll, 2),
                "fonte": "webscraping_multiplo"
            }
            
            logger.info(f"✅ Webscraping múltiplo concluído: {total_distance}km, R${total_toll}")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro no webscraping múltiplo: {e}")
            return {
                "origem": origem,
                "destino": ", ".join(destinos),
                "distance": 0,
                "pedagios": 0,
                "fonte": "erro_webscraping_multiplo"
            }
