import os
import requests

from src.infrastructure.safe_console import safe_console_line


class N8NClient:
    def __init__(self):
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL")
        safe_console_line(f"DEBUG: URL n8n chargée depuis le .env -> {self.webhook_url}")

    def trigger_workflow(self, data: dict):
        if not self.webhook_url:
            return {"status": "error", "message": "N8N_WEBHOOK_URL non configuré dans le .env"}

        try:
            safe_console_line(f"[N8N] Envoi payload vers n8n: {data}")
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            json_response = response.json()
            safe_console_line(f"[N8N] Réponse n8n (HTTP {response.status_code}): {json_response}")
            return json_response
        except Exception as e:
            safe_console_line(f"[N8N] Erreur lors de l'appel n8n: {str(e)}")
            return {"status": "error", "message": str(e)}