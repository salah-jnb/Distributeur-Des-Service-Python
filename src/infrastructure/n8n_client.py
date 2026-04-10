import requests
import os


class N8NClient:
    def __init__(self):
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL")
        # AJOUTE CETTE LIGNE POUR VÉRIFIER :
        print(f"DEBUG: URL n8n chargée depuis le .env -> {self.webhook_url}")
    def trigger_workflow(self, data: dict):
        if not self.webhook_url:
            return {"status": "error", "message": "N8N_WEBHOOK_URL non configuré dans le .env"}

        try:
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}