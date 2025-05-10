from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tenacity import retry, stop_after_attempt, wait_fixed
from selenium.common.exceptions import WebDriverException
import time
import concurrent.futures
import os
from pathlib import Path

DOWNLOAD_DIR = os.path.join(os.getcwd(), "data")

def wait_download(download_dir, name_file, timeout=60):
    path_file = Path(download_dir) / name_file
    start = time.time()
    while not path_file.exists():
        if time.time() - start > timeout:
            raise TimeoutError(f"Download do arquivo '{name_file}' não concluído após {timeout} segundos.")
        time.sleep(1)
            

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1), reraise=True)
def download_file(url, recursos_button, selector_button_download, name_thread):
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
        time.sleep(4)
        if recursos_button is not None:
            recursos = wait.until(EC.element_to_be_clickable((By.XPATH, recursos_button)))
            recursos.click()
        print(f"[{name_thread}] Iniciando download...")
        download = wait.until(EC.element_to_be_clickable((By.XPATH, selector_button_download))).click()
        
        print(f"[{name_thread}] Aguardando download concluir...")
        if name_thread == "obitos_confirmados_coronavirus":
            wait_download(DOWNLOAD_DIR, "obitos-confirmados-covid-19.csv")
        elif name_thread == "casos_coronavirus":
            wait_download(DOWNLOAD_DIR, "XLSX_Painel_2020.xlsx")
            
        print(f"[{name_thread}] Download concluído.")
        
    except Exception as e:  
        print(f"[{name_thread}] Erro: {e}")
        raise
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
        "url": "https://sescloud.saude.mg.gov.br/index.php/s/ZEzzC8jFpobXGjM?path=%2FPAINEL_COVID",
        "recursos_button": None,
        "selector_button_download": '//*[@id="fileList"]/tr[2]/td[2]/a',
        "name_thread": "casos_coronavirus" 
    }
]


def run_threads():
    os.makedirs('data', exist_ok=True)
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
                
                
                
