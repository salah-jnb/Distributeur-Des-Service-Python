from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Activity:
    id: int
    titre: str
    description: str
    etat: bool
    date: str
    created_at: Optional[datetime] = None
