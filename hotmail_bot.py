import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def digita_devagar(elemento, texto):
    for letra in texto:
        elemento.send_keys(letra)
        time.sleep(random.uniform(0.1, 0.25))

EMAIL = "brunobfs_santos@hotmail.com"
SENHA = "130142350622Br@#"

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options)

try:
    driver.get("https://login.live.com/")
    time.sleep(3)

    # Campo de e-mail usando name="loginfmt"
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "usernameEntry"))
    )
    digita_devagar(email_input, EMAIL)
    driver.find_element(By.ID, "idSIButton9").click()  # botão "Avançar"

    # Campo de senha
    senha_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "passwd"))
    )
    digita_devagar(senha_input, SENHA)
    driver.find_element(By.ID, "idSIButton9").click()  # botão "Entrar"

    # "Manter conectado?" - clicar em "Não"
    try:
        nao_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "idBtn_Back"))
        )
        nao_btn.click()
    except:
        pass

    # Aguarda a caixa de entrada do Outlook carregar
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='main']"))
    )
    time.sleep(10)

    # Localiza e-mails com assunto contendo "Confirmação"
    assuntos = driver.find_elements(By.XPATH, "//span[contains(text(),'Confirmação')]")
    print(f"📩 Encontrados {len(assuntos)} e-mails com assunto 'Confirmação':")
    for a in assuntos:
        print(" -", a.text)

except Exception as e:
    print("❌ Erro durante o processo:", e)

finally:
    time.sleep(10)
    driver.quit()
