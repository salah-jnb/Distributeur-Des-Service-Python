from src.presentation.services_interfaces import IApiService
from src.infrastructure.database import get_supabase_client
from src.infrastructure.n8n_client import N8NClient

class ApiServiceImpl(IApiService):
    def __init__(self):
        # Initialisation obligatoire des deux clients
        self.client = get_supabase_client()
        self.n8n = N8NClient()

    # --- UTILISATEURS ---
    def get_all_users(self):
        return self.client.table("utilisateur").select("*").execute().data

    def delete_user(self, user_id: int):
        return self.client.table("utilisateur").delete().eq("id", user_id).execute().data

    # --- HISTORIQUE ---
    def get_all_history(self):
        return self.client.table("historique").select("*").execute().data

    # --- CONVERSATIONS ---
    def get_last_100_conversations(self):
        return self.client.table("conversation").select("*").order("date", desc=True).limit(100).execute().data

    # --- NOTES ---
    def get_all_notes(self):
        return self.client.table("note").select("*").execute().data

    def modify_note_etat(self, note_id: int, etat: bool):
        return self.client.table("note").update({"etat": etat}).eq("id", note_id).execute().data

    # --- SETTINGS ---
    def get_settings(self):
        res = self.client.table("setting").select("*").limit(1).execute().data
        return res[0] if res else None

    def modify_settings(self, settings_data: dict):
        return self.client.table("setting").update(settings_data).eq("id", 1).execute().data

    # --- INFOS PERSONNELLES ---
    def get_personal_info(self):
        return self.client.table("information_personelle").select("*").execute().data

    def add_personal_info(self, info_data: dict):
        return self.client.table("information_personelle").insert(info_data).execute().data

    # --- INTEGRATION N8N ---
    def send_to_n8n(self, payload: dict):
        # Cette fois-ci, self.n8n est bien défini dans le __init__ au-dessus
        return self.n8n.trigger_workflow(payload)