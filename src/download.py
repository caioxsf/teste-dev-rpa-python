from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import concurrent.futures
import os

DOWNLOAD_DIR = os.path.join(os.getcwd(), "data")

def download_file(url, recursos_button, selector_button_download, name_thread):
    print(f"[{name_thread}] Iniciando...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        # clicar pra abrir o recursos 
        recursos = wait.until(EC.element_to_be_clickable((By.XPATH, recursos_button))).click()
        # faz o download da bombeta do csv ;----------;
        download = wait.until(EC.element_to_be_clickable((By.XPATH, selector_button_download))).click()
        
        # ( eu sei que era melhor fazer uma função pra verificar se não terminou o download por conta de arquivos grandes :) )
        time.sleep(10)
        print(f"[{name_thread}] Download concluído.")
        
    except Exception as e:
        print(f"[{name_thread}] Erro: {e}")
    finally:
        driver.quit()
        
sites = [
    {
        "url": "https://dados.gov.br/dados/conjuntos-dados/obitos-confirmados-covid-19",
        "recursos_button": '(//*[@id="btnCollapse"])[3]',
        "selector_button_download": '(//*[@id="btnDownloadUrl"])[2]',
        "name_thread": "obitos_confirmados_coronavirus"
    },
    {
        "url": "https://dados.gov.br/dados/conjuntos-dados/contratos-covid-19",
        "recursos_button": '(//*[@id="btnCollapse"])[3]',
        "selector_button_download": '(//*[@id="btnDownloadUrl"])[1]',
        "name_thread": "contratos_coronavirus"
    }
]

def run_threads():
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sites)) as executor:
        futures = [
            executor.submit(download_file, site["url"], site["recursos_button"], site["selector_button_download"], site["name_thread"])
            for site in sites
        ]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Erro em uma das threads: {e}")
                
