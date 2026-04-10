from dataclasses import dataclass
@dataclass
class Note:
    id: int
    note: str
    etat: bool