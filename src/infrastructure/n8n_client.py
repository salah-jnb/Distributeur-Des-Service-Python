import os
import requests

from src.infrastructure.safe_console import safe_console_line


class N8NClient:
    def __init__(self):
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL")
        safe_console_line(f"DEBUG: URL n8n chargée depuis le .env -> {self.webhook_url}")

    def trigger_workflow(self, data: dict):
        """Backward-compatible: returns parsed JSON if possible, otherwise dict with raw text."""
        if not self.webhook_url:
            return {"status": "error", "message": "N8N_WEBHOOK_URL non configuré dans le .env"}

        try:
            safe_console_line(f"[N8N] Envoi payload vers n8n: {data}")
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            content_type = (response.headers.get("content-type") or "").lower()
            if "application/json" in content_type:
                payload = response.json()
                safe_console_line(f"[N8N] Réponse n8n JSON (HTTP {response.status_code}): {payload}")
                return payload
            # Plain text responses ("I am Closed ", "Yo Yo", "direction\navant", …).
            text_body = response.text
            safe_console_line(f"[N8N] Réponse n8n TEXT (HTTP {response.status_code}): {text_body!r}")
            return text_body
        except Exception as e:
            safe_console_line(f"[N8N] Erreur lors de l'appel n8n: {str(e)}")
            return {"status": "error", "message": str(e)}

    def trigger_workflow_raw(self, data: dict):
        """
        Returns a structured envelope so callers can inspect content_type and dispatch
        on response shape. Used by the action-dispatcher pipeline (multi-type replies:
        text / music / motion / sleep).
        """
        if not self.webhook_url:
            return {
                "ok": False,
                "content_type": None,
                "status_code": None,
                "json": None,
                "text": None,
                "error": "N8N_WEBHOOK_URL non configuré dans le .env",
            }
        try:
            safe_console_line(f"[N8N] (raw) Envoi payload vers n8n: {data}")
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            content_type = (response.headers.get("content-type") or "").lower()
            envelope = {
                "ok": True,
                "content_type": content_type,
                "status_code": response.status_code,
                "json": None,
                "text": response.text,
                "error": None,
            }
            if "application/json" in content_type:
                try:
                    envelope["json"] = response.json()
                except ValueError:
                    pass
            safe_console_line(
                f"[N8N] (raw) Réponse (HTTP {response.status_code}, type={content_type!r}): "
                f"{(envelope['json'] if envelope['json'] is not None else envelope['text'])!s}"
            )
            return envelope
        except Exception as e:
            safe_console_line(f"[N8N] (raw) Erreur lors de l'appel n8n: {str(e)}")
            return {
                "ok": False,
                "content_type": None,
                "status_code": None,
                "json": None,
                "text": None,
                "error": str(e),
            }