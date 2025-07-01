import requests

TELEGRAM_TOKEN = "COLE_O_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "7521702072"

mensagem = "🚀 Teste de envio do bot!"
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}

resposta = requests.post(url, json=payload)
print(resposta.status_code)
print(resposta.text)
