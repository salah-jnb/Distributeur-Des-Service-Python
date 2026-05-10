from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---- AGENDA ----
class AgendaCreate(BaseModel):
    titre: str
    note: str
    etat: bool = False
    contenu: str
    date_modification: Optional[datetime] = None

class AgendaUpdate(BaseModel):
    titre: Optional[str] = None
    note: Optional[str] = None
    etat: Optional[bool] = None
    contenu: Optional[str] = None
    date_modification: Optional[datetime] = None


# ---- ACTIVITY ----
class ActivityCreate(BaseModel):
    titre: str
    description: str
    etat: bool = False
    date: str

class ActivityUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    etat: Optional[bool] = None
    date: Optional[str] = None


# ---- SETTING (table setting / paramètres robot) ----
class SettingUpdate(BaseModel):
    name: Optional[str] = None
    sexe: Optional[str] = None
    date: Optional[str] = None
    motdepasse: Optional[str] = None
    etat: Optional[bool] = None
    caractere: Optional[str] = None
    langue: Optional[str] = None


# ---- AUDIO ----
class TextToSpeechRequest(BaseModel):
    text: str
    voice_name: Optional[str] = None
