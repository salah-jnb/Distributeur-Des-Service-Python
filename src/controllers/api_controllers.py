from fastapi import APIRouter, HTTPException
from src.application.app_service_impl import ApiServiceImpl

router = APIRouter()
service = ApiServiceImpl()

# Endpoints Utilisateurs
@router.get("/users")
def get_users():
    return service.get_all_users()

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return service.delete_user(user_id)

# Endpoints Historique
@router.get("/history")
def get_history():
    return service.get_all_history()

# Endpoints Conversations
@router.get("/conversations/last100")
def get_convs():
    return service.get_last_100_conversations()

# Endpoints Notes
@router.get("/notes")
def get_notes():
    return service.get_all_notes()

@router.patch("/notes/{note_id}/etat")
def update_note(note_id: int, etat: bool):
    return service.modify_note_etat(note_id, etat)

# Endpoints Settings
@router.get("/settings")
def get_settings():
    return service.get_settings()

@router.put("/settings")
def update_settings(data: dict):
    return service.modify_settings(data)

@router.get("/personal-info")
def get_all_info():
    return service.get_personal_info()

@router.post("/personal-info")
def save_info(data: dict):
    return service.add_personal_info(data)

# Endpoint pour déclencher n8n
@router.post("/trigger-n8n")
def trigger_n8n_workflow(payload: dict):
    """
    Envoie n'importe quelle donnée à n8n (ex: une question pour traitement IA)
    """
    return service.send_to_n8n(payload)