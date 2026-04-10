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