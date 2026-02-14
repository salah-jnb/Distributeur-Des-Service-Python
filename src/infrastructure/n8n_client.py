import requests
from src.config.config import settings

class N8NClient:
    def __init__(self):
        self.url = settings.N8N_URL

    def send_to_workflow(self, user_question: str, user_id: str):
        payload = {
            "chatInput": user_question,
            "userId": user_id
        }
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur n8n: {e}")
            return None