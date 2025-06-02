import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

def digita_devagar(elemento, texto):
    for letra in texto:
        elemento.send_keys(letra)
        time.sleep(random.uniform(0.1, 0.3))

EMAIL = "senseregistros+brunoFERREIRADOSsantos@gmail.com"
SENHA = "Cidadania10"

# Altere isso para o caminho do seu perfil Chrome
chrome_profile = os.path.expanduser(r"C:\Users\marcio.leite\AppData\Local\Google\Chrome\User Data\Default")

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--lang=it-IT")
options.add_argument(f"--user-data-dir={chrome_profile}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

try:
    driver = uc.Chrome(options=options)
    driver.get("https://prenotami.esteri.it")
    time.sleep(random.uniform(3, 5))

    email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "login-email")))
    email_field.clear()
    email_field.send_keys(u'\ue009' + 'a')  # Ctrl+A
    email_field.send_keys(u'\ue003')        # Delete
    time.sleep(0.5)
    if email_field.get_attribute("value"):
        email_field.clear()
    time.sleep(random.uniform(1, 2))
    digita_devagar(email_field, EMAIL)

    senha_field = driver.find_element(By.ID, "login-password")
    senha_field.clear()
    senha_field.send_keys(u'\ue009' + 'a')  # Ctrl+A
    senha_field.send_keys(u'\ue003')        # Delete
    time.sleep(0.5)
    if senha_field.get_attribute("value"):
        senha_field.clear()
    time.sleep(random.uniform(1, 2))
    digita_devagar(senha_field, SENHA)

    login_btn = driver.find_element(By.XPATH, '//*[@id="login-form"]/button')
    time.sleep(random.uniform(1, 2))
    login_btn.click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="advanced"]/span')))
    time.sleep(random.uniform(1, 2))
    driver.find_element(By.XPATH, '//*[@id="advanced"]/span').click()

    print("✅ Sucesso!")

except Exception as e:
    print("❌ Erro:", e)

finally:
    time.sleep(10)
    try:
        driver.quit()
    except:
        pass
