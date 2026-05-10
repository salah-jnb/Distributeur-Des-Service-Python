from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from src.application.app_service_impl import ApiServiceImpl
from src.controllers.schemas import (
    AgendaCreate,
    AgendaUpdate,
    ActivityCreate,
    ActivityUpdate,
    SettingUpdate,
    TextToSpeechRequest,
)

router = APIRouter()
service = ApiServiceImpl()

# ==============================================================
# ENDPOINTS UTILISATEURS
# ==============================================================
@router.get("/users", summary="Lister tous les utilisateurs")
def get_users():
    return service.get_all_users()

@router.delete("/users/{user_id}", summary="Supprimer un utilisateur")
def delete_user(user_id: int):
    return service.delete_user(user_id)

# ==============================================================
# ENDPOINTS HISTORIQUE
# ==============================================================
@router.get("/history", summary="Lister tout l'historique")
def get_history():
    return service.get_all_history()

# ==============================================================
# ENDPOINTS CONVERSATIONS
# ==============================================================
@router.get("/conversations/last100", summary="100 dernières conversations")
def get_convs():
    return service.get_last_100_conversations()

# ==============================================================
# ENDPOINTS NOTES
# ==============================================================
@router.get("/notes", summary="Lister toutes les notes")
def get_notes():
    return service.get_all_notes()

@router.patch("/notes/{note_id}/etat", summary="Modifier l'état d'une note")
def update_note(note_id: int, etat: bool):
    return service.modify_note_etat(note_id, etat)

# ==============================================================
# ENDPOINTS SETTINGS
# ==============================================================
@router.get("/settings", summary="Obtenir les paramètres")
def get_settings():
    return service.get_settings()

@router.put("/settings", summary="Modifier les paramètres")
def update_settings(data: SettingUpdate):
    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise HTTPException(status_code=400, detail="Aucun champ à mettre à jour")
    return service.modify_settings(payload)

# ==============================================================
# ENDPOINTS INFORMATIONS PERSONNELLES
# ==============================================================
@router.get("/personal-info", summary="Obtenir les informations personnelles")
def get_all_info():
    return service.get_personal_info()

@router.post("/personal-info", summary="Ajouter des informations personnelles")
def save_info(data: dict):
    return service.add_personal_info(data)

# ==============================================================
# ENDPOINT N8N
# ==============================================================
@router.post("/trigger-n8n", summary="Déclencher un workflow n8n")
def trigger_n8n_workflow(payload: dict):
    """Envoie n'importe quelle donnée à n8n (ex: une question pour traitement IA)"""
    return service.send_to_n8n(payload)

# ==============================================================
# ENDPOINTS AGENDA (CRUD complet)
# ==============================================================
@router.get("/agendas", summary="Lister tous les agendas")
def get_agendas():
    return service.get_all_agendas()

@router.get("/agendas/{agenda_id}", summary="Obtenir un agenda par ID")
def get_agenda(agenda_id: int):
    result = service.get_agenda(agenda_id)
    if not result:
        raise HTTPException(status_code=404, detail="Agenda introuvable")
    return result

@router.post("/agendas", summary="Créer un agenda", status_code=201)
def create_agenda(data: AgendaCreate):
    return service.create_agenda(data.model_dump(exclude_none=True))

@router.put("/agendas/{agenda_id}", summary="Mettre à jour un agenda")
def update_agenda(agenda_id: int, data: AgendaUpdate):
    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise HTTPException(status_code=400, detail="Aucune donnée fournie")
    return service.update_agenda(agenda_id, payload)

@router.delete("/agendas/{agenda_id}", summary="Supprimer un agenda")
def delete_agenda(agenda_id: int):
    return service.delete_agenda(agenda_id)

# ==============================================================
# ENDPOINTS ACTIVITY (CRUD complet)
# ==============================================================
@router.get("/activities", summary="Lister toutes les activités")
def get_activities():
    return service.get_all_activities()

@router.get("/activities/{activity_id}", summary="Obtenir une activité par ID")
def get_activity(activity_id: int):
    result = service.get_activity(activity_id)
    if not result:
        raise HTTPException(status_code=404, detail="Activité introuvable")
    return result

@router.post("/activities", summary="Créer une activité", status_code=201)
def create_activity(data: ActivityCreate):
    return service.create_activity(data.model_dump(exclude_none=True))

@router.put("/activities/{activity_id}", summary="Mettre à jour une activité")
def update_activity(activity_id: int, data: ActivityUpdate):
    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise HTTPException(status_code=400, detail="Aucune donnée fournie")
    return service.update_activity(activity_id, payload)

@router.delete("/activities/{activity_id}", summary="Supprimer une activité")
def delete_activity(activity_id: int):
    return service.delete_activity(activity_id)

# ==============================================================
# ENDPOINT RECONNAISSANCE FACIALE
# ==============================================================
@router.post("/identify-face", summary="Identifier une personne par reconnaissance faciale")
async def identify_face(file: UploadFile = File(...)):
    """
    Reçoit une image (photo), la compare aux photos de tous les utilisateurs
    stockées dans Supabase Storage, et retourne le nom de la personne identifiée
    ou 'inconnu' si elle n'est pas reconnue.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image")
    image_bytes = await file.read()
    try:
        name = service.identify_face(image_bytes)
        return {"nom": name}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la reconnaissance: {str(e)}")

# ==============================================================
# ENDPOINTS POWER ON / OFF
# ==============================================================
@router.post("/power-off", summary="Éteindre le système (etat = 0)")
def power_off():
    """
    Met le champ 'etat' dans la table setting à 0 (False).
    Signifie que le robot/distributeur est éteint.
    """
    return service.power_off()

@router.post("/power-on", summary="Allumer le système (etat = 1)")
def power_on():
    """
    Met le champ 'etat' dans la table setting à 1 (True).
    Signifie que le robot/distributeur est allumé.
    """
    return service.power_on()


# ==============================================================
# ENDPOINTS AUDIO (AZURE SPEECH)
# ==============================================================
@router.post("/audio/speech-to-text", summary="Convertir un fichier audio en texte")
async def speech_to_text(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un audio")

    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Le fichier audio est vide")

    try:
        return service.speech_to_text(audio_bytes)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Speech-to-Text: {str(e)}")


@router.post("/audio/text-to-speech", summary="Convertir du texte en audio")
def text_to_speech(payload: TextToSpeechRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Le texte ne doit pas être vide")

    try:
        audio_data = service.text_to_speech(payload.text, payload.voice_name)
        return StreamingResponse(
            iter([audio_data]),
            media_type="audio/wav",
            headers={"Content-Disposition": "inline; filename=tts.wav"}
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Text-to-Speech: {str(e)}")


@router.post("/audio/speech-to-n8n-to-speech", summary="Audio -> texte -> n8n -> audio")
async def speech_to_n8n_to_speech(
    file: UploadFile = File(...),
    voice_name: str = Form(None),
    extra_text: str = Form(
        None,
        description="Texte ajouté entre parenthèses après la question STT, ex. « bonjour (oussema) »",
    ),
):
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un audio")

    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Le fichier audio est vide")

    try:
        result = service.audio_to_n8n_to_audio(audio_bytes, voice_name, extra_text)
        return StreamingResponse(
            iter([result["audio_bytes"]]),
            media_type="audio/wav",
            headers={"Content-Disposition": "inline; filename=n8n_reply.wav"}
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        try:
            detail = f"Erreur pipeline audio n8n: {e!s}"
        except Exception:
            detail = "Erreur pipeline audio n8n."
        raise HTTPException(status_code=500, detail=detail)


# ==============================================================
# ENDPOINT GEMINI KEYWORDS (ROBOT NAME)
# ==============================================================
@router.get("/keywords/robot-name", summary="Générer les variantes du nom du robot via Gemini")
def get_robot_name_keywords():
    try:
        return service.generate_robot_name_keywords()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Gemini keywords: {str(e)}")