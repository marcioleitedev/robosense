import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import random
import os

# --- CONFIG TELEGRAM ---
TELEGRAM_TOKEN = "7858429749:AAEpEhYqhZIZg1ixVRDOt1yyms83vwtA3zo"
TELEGRAM_CHAT_ID = "7521702072"  


def digita_devagar(elemento, texto):
    for letra in texto:
        elemento.send_keys(letra)
        time.sleep(random.uniform(0.1, 0.3))

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Mensagem enviada via Telegram!")
        else:
            print(f"⚠️ Falha ao enviar mensagem Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Erro ao enviar Telegram: {e}")

EMAIL = "senseregistros+brunoferreiradossantos@gmail.com"
SENHA = "Cidadania10"

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

encontrou = False

try:
    driver = uc.Chrome(options=options)
    driver.get("https://prenotami.esteri.it")
    time.sleep(random.uniform(3, 5))

    email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "login-email")))
    email_field.clear()
    email_field.send_keys(u'\ue009' + 'a')
    email_field.send_keys(u'\ue003')
    time.sleep(0.5)
    if email_field.get_attribute("value"):
        email_field.clear()
    time.sleep(random.uniform(1, 2))
    digita_devagar(email_field, EMAIL)

    senha_field = driver.find_element(By.ID, "login-password")
    senha_field.clear()
    senha_field.send_keys(u'\ue009' + 'a')
    senha_field.send_keys(u'\ue003')
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

    try:
        tbody = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//table//tbody'))
        )
        WebDriverWait(driver, 20).until(
            lambda d: len(tbody.find_elements(By.TAG_NAME, "tr")) > 0
        )

        linhas = tbody.find_elements(By.TAG_NAME, "tr")
        print("✅ Tabela carregada com sucesso (tbody).")
        print(f"Total de linhas encontradas: {len(linhas)}")

        for i, linha in enumerate(linhas):
            classe_linha = linha.get_attribute("class")
            if classe_linha != "odd":
                continue

            tds = linha.find_elements(By.TAG_NAME, "td")
            for td in tds:
                if "Agendamento Primeiro Passaporte" in td.text:
                    encontrou = True
                    print("✅ Encontrado: Agendamento Primeiro Passaporte")

                    if i + 1 < len(linhas):
                        proxima_linha = linhas[i + 1]
                        try:
                            reservar_link = proxima_linha.find_element(
                                By.XPATH,
                                './/a[contains(@href, "/Services/Booking/")]/button[contains(text(), "Reservar")]'
                            )
                            time.sleep(random.uniform(1, 2))
                            driver.execute_script("arguments[0].click();", reservar_link)
                            print("✅ Clique no botão Reservar realizado!")
                        except Exception as e:
                            print("⚠️ Não foi possível clicar no botão Reservar:", e)
                    else:
                        print("⚠️ Não há próxima linha para clicar em Reservar.")
                    break

            if encontrou:
                break

        if not encontrou:
            print("❌ Agendamento Primeiro Passaporte não encontrado na tabela.")

    except Exception as e:
        print("❌ Erro ao processar a tabela:", e)

except Exception as e:
    print("❌ Erro geral:", e)

finally:
    mensagem_final = "✅ Reservado com sucesso!" if encontrou else "❌ Nenhuma vaga encontrada."
    enviar_telegram(mensagem_final)

    time.sleep(10)
    try:
        driver.quit()
    except:
        pass
    print("✅ Navegador fechado.")
    print("✅ Script finalizado.")
