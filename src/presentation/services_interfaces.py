from abc import ABC, abstractmethod

class IApiService(ABC):
    # Utilisateurs
    @abstractmethod
    def get_all_users(self): pass
    @abstractmethod
    def delete_user(self, user_id: int): pass

    # Historique
    @abstractmethod
    def get_all_history(self): pass

    # Conversations
    @abstractmethod
    def get_last_100_conversations(self): pass

    # Notes
    @abstractmethod
    def get_all_notes(self): pass
    @abstractmethod
    def modify_note_etat(self, note_id: int, etat: bool): pass

    # Settings
    @abstractmethod
    def get_settings(self): pass
    @abstractmethod
    def modify_settings(self, settings_data: dict): pass

    # Agenda
    @abstractmethod
    def get_all_agendas(self): pass
    @abstractmethod
    def get_agenda(self, agenda_id: int): pass
    @abstractmethod
    def create_agenda(self, data: dict): pass
    @abstractmethod
    def update_agenda(self, agenda_id: int, data: dict): pass
    @abstractmethod
    def delete_agenda(self, agenda_id: int): pass

    # Activity
    @abstractmethod
    def get_all_activities(self): pass
    @abstractmethod
    def get_activity(self, activity_id: int): pass
    @abstractmethod
    def create_activity(self, data: dict): pass
    @abstractmethod
    def update_activity(self, activity_id: int, data: dict): pass
    @abstractmethod
    def delete_activity(self, activity_id: int): pass

    # Reconnaissance faciale
    @abstractmethod
    def identify_face(self, image_bytes: bytes): pass

    # Power on/off
    @abstractmethod
    def power_off(self): pass
    @abstractmethod
    def power_on(self): pass

    # Audio (Azure Speech)
    @abstractmethod
    def speech_to_text(self, audio_bytes: bytes): pass
    @abstractmethod
    def text_to_speech(self, text: str, voice_name=None): pass
    @abstractmethod
    def audio_to_n8n_to_audio(self, audio_bytes: bytes, voice_name=None, extra_text=None): pass

    # Gemini keywords
    @abstractmethod
    def generate_robot_name_keywords(self): pass