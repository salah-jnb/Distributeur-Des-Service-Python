from dataclasses import dataclass
@dataclass
class Setting:
    id: int
    name: str
    sexe: str
    date: str
    motdepasse: str
    etat: bool
    caractere: str