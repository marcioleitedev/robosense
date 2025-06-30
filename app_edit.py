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

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Telegram enviado!")
        else:
            print(f"⚠️ Erro Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Erro ao enviar Telegram: {e}")

def digita_devagar(elemento, texto):
    for letra in texto:
        elemento.send_keys(letra)
        time.sleep(random.uniform(0.05, 0.2))

EMAIL = "senseregistros+brunoferreiradossantos@gmail.com"
SENHA = "Cidadania10"
chrome_profile = os.path.expanduser(r"C:\Users\marcio.leite\AppData\Local\Google\Chrome\User Data")

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--lang=it-IT")
options.add_argument(f"--user-data-dir={chrome_profile}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-blink-features=AutomationControlled")

MAX_TENTATIVAS = 10
tentativas = 0
agendado = False

while tentativas < MAX_TENTATIVAS and not agendado:
    tentativas += 1
    print(f"\n🔁 Tentativa {tentativas}/{MAX_TENTATIVAS}")
    driver = None

    try:
        driver = uc.Chrome(options=options)
        driver.get("https://prenotami.esteri.it")
        time.sleep(random.uniform(3, 5))

        # LIMPAR E PREENCHER E-MAIL
        email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "login-email")))
        email_field.clear()
        time.sleep(0.5)
        digita_devagar(email_field, EMAIL)

        # LIMPAR E PREENCHER SENHA
        senha_field = driver.find_element(By.ID, "login-password")
        senha_field.clear()
        time.sleep(0.5)
        digita_devagar(senha_field, SENHA)

        # CLICAR EM LOGIN
        login_btn = driver.find_element(By.XPATH, '//*[@id="login-form"]/button')
        time.sleep(random.uniform(1, 2))
        login_btn.click()

        # CLICAR EM SERVIÇOS AVANÇADOS
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="advanced"]/span')))
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="advanced"]/span').click()

        # AGUARDAR TABELA CARREGAR
        tbody = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//table//tbody')))
        WebDriverWait(driver, 20).until(lambda d: len(tbody.find_elements(By.TAG_NAME, "tr")) > 0)

        linhas = tbody.find_elements(By.TAG_NAME, "tr")
        print(f"✅ Linhas encontradas: {len(linhas)}")

        for i, linha in enumerate(linhas):
            if linha.get_attribute("class") != "odd":
                continue

            tds = linha.find_elements(By.TAG_NAME, "td")
            for td in tds:
                if "Agendamento Primeiro Passaporte" in td.text:
                    print("✅ Agendamento disponível!")

                    if i + 1 < len(linhas):
                        proxima_linha = linhas[i + 1]
                        try:
                            reservar_link = proxima_linha.find_element(By.XPATH, ".//a[contains(text(), 'Prenota')]")
                            time.sleep(random.uniform(1, 2))
                            driver.execute_script("arguments[0].click();", reservar_link)
                            print("✅ Clicou em Reservar.")

                            # AGUARDAR NOVA PÁGINA
                            try:
                                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="PrivacyCheck"]')))
                                print("⏳ Nova página carregada. Aguardando 45s...")
                                time.sleep(45)

                                driver.find_element(By.XPATH, '//*[@id="PrivacyCheck"]').click()
                                print("✅ Clicou em PrivacyCheck.")

                                driver.find_element(By.XPATH, '//*[@id="otp-send"]').click()
                                print("✅ Clicou em otp-send.")

                                msg = f"✅ Agendamento realizado com sucesso para: {EMAIL}"
                                enviar_telegram(msg)
                                agendado = True
                                break

                            except Exception as e:
                                print("❌ Nova página não carregou corretamente.")
                                enviar_telegram(f"⚠️ ERRO: Página após Reservar não carregou para {EMAIL}")
                                break

                        except Exception as e:
                            print("⚠️ Erro ao clicar em Prenota:", e)
                    else:
                        print("⚠️ Não encontrou linha para clicar em Reservar.")
                    break
            if agendado:
                break

        if not agendado:
            print("❌ Agendamento não feito. Fechando navegador e tentando novamente...")
            driver.quit()
            time.sleep(5)

    except Exception as e:
        print(f"❌ Erro geral na tentativa {tentativas}: {e}")
        try:
            if driver:
                driver.quit()
        except:
            pass
        time.sleep(5)

# FINALIZAÇÃO
if not agendado:
    enviar_telegram(f"❌ Não conseguimos agendar após {MAX_TENTATIVAS} tentativas para o e-mail: {EMAIL}")
else:
    print("✅ Processo concluído com sucesso.")
