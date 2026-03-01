
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Get bot token and chat id
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN_STUDENT_JOBS"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID_STUDENT_JOBS"]

# Send a message with string
def send_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, json=payload)
    return response.ok
