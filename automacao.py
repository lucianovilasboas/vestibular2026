from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from log import logger

# Configurar a pasta de download
download_dir = "/mnt/Data/Dev/python_projects/vestibular2026/dados/input"

# Configura as opções do Chrome para definir a pasta de download
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,  # Diretório onde o arquivo será salvo
    "download.prompt_for_download": False,  # Baixar automaticamente sem perguntar
    "download.directory_upgrade": True,  # Atualiza o diretório
    "safebrowsing.enabled": True  # Evitar alertas de segurança de navegação
}
chrome_options.add_experimental_option("prefs", prefs)

# Configurações para o modo headless
# chrome_options.add_argument("--headless")  # Executa sem interface gráfica
# chrome_options.add_argument("--disable-gpu")  # Necessário em alguns sistemas
# chrome_options.add_argument("--no-sandbox")  # Segurança para o ambiente de execução

# Configurando o ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)


url = "https://fundacao.cefetmg.br/login"
# Acessa a página de login
driver.get(url)

driver.maximize_window()

# Preenche o campo de login
username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
if (username_input.is_displayed()):
    username_input.send_keys("04977219619") # inserir o codigo de acesso

# Preenche o campo de senha
password_input = driver.find_element(By.NAME, "password")
if(password_input.is_displayed()):
    password_input.send_keys("wckC6Dch3y") # inseir a senha

# Clica no botão de login
login_button = driver.find_element(By.CSS_SELECTOR, "#login-box > form > div.footer > button")
if(login_button.is_displayed()):
    login_button.click()


driver.get(url)
time.sleep(1)

# Seleciona o campo select e extrai as opções
try:

    # Download 1
    select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > header > nav > div > ul > li.dropdown.messages-menu > a")))
    if select.is_displayed():
        select.click()
    logger.info(f"Dropdown exibido...")

    # Acessa o painel de detalhamento
    painel = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.row-offcanvas.row-offcanvas-left > aside.right-side > section.content > h2 > a")
    if(painel.is_displayed()):
        painel.click()
    download_csv = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.row-offcanvas.row-offcanvas-left > aside.right-side > section.content > div.box.box-success > div.box-header > div > a")
    if(download_csv.is_displayed()):
        download_csv.click()    


    time.sleep(2)
    
    
    # Download 2
    select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > header > nav > div > ul > li.dropdown.messages-menu > a")))
    if select.is_displayed():
        select.click()
    logger.info(f"Dropdown exibido...")

    painel = driver.find_element(By.CSS_SELECTOR, "body > header > nav > div > ul > li.dropdown.messages-menu.open > ul > li:nth-child(2) > div > ul > li:nth-child(2) > a")
    if(painel.is_displayed()):
        painel.click()

    # Acessa o painel de detalhamento
    painel = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.row-offcanvas.row-offcanvas-left > aside.right-side > section.content > h2 > a")
    if(painel.is_displayed()):
        painel.click()    

    download_csv = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.row-offcanvas.row-offcanvas-left > aside.right-side > section.content > div.box.box-success > div.box-header > div > a")
    if(download_csv.is_displayed()):
        download_csv.click()  

    time.sleep(2)



    # Download 3
    select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > header > nav > div > ul > li.dropdown.messages-menu > a")))
    if select.is_displayed():
        select.click()
    logger.info(f"Dropdown exibido...")

    painel = driver.find_element(By.CSS_SELECTOR, "body > header > nav > div > ul > li.dropdown.messages-menu.open > ul > li:nth-child(2) > div > ul > li:nth-child(3) > a")
    if(painel.is_displayed()):
        painel.click()

    # Acessa o painel de detalhamento
    painel = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.row-offcanvas.row-offcanvas-left > aside.right-side > section.content > h2 > a")
    if(painel.is_displayed()):
        painel.click()

    download_csv = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper.row-offcanvas.row-offcanvas-left > aside.right-side > section.content > div.box.box-success > div.box-header > div > a")
    if(download_csv.is_displayed()):
        download_csv.click()  



    time.sleep(3)



except Exception as e:
    print(f"Erro ao acessar o painel de detalhamento: {e}")
    logger.error(f"Erro ao acessar o painel de detalhamento: {e}")


# Fecha o navegador após completar o processo
driver.quit()
