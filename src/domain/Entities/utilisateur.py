from dataclasses import dataclass

@dataclass
class Utilisateur:
    id: int
    nom: str
    image: str # URL du bucket photo_utilisateurs