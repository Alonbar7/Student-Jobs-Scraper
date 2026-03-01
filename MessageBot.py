
import requests

# Bot class for telegram
class MessageBot:
    
    def __init__(self, token, chat_id):
        
        self.BOT_TOKEN = token
        self.CHAT_ID = chat_id

    # Send a message with string
    def send_message(self, text: str):
        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
        payload = {"chat_id": self.CHAT_ID, "text": text}
        response = requests.post(url, json=payload)
        return response.ok
