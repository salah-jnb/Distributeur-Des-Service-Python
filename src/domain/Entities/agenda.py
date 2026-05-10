from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Agenda:
    id: int
    titre: str
    note: str
    etat: bool
    contenu: str
    date_modification: Optional[datetime] = None
