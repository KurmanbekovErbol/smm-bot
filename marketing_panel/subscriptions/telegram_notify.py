import requests
from django.conf import settings

BOT_TOKEN = '8599455727:AAGlzDt202yNUdhSy7chOQWjlR20e2opuTs'  # твой токен

def notify_user(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    print("=== TELEGRAM DEBUG ===")
    print("Sending to chat_id:", chat_id)
    print("URL:", url)

    try:
        r = requests.post(url, data=payload, timeout=5)
        print("Status code:", r.status_code)
        print("Response:", r.text)
        print("======================")

        return r.status_code == 200

    except Exception as e:
        print("ERROR sending:", e)
        print("======================")
        return False
