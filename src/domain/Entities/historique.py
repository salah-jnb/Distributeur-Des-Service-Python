from dataclasses import dataclass
from datetime import datetime
@dataclass
class Historique:
    id: int
    created_at: datetime
    question: str
    reponce: str
    typedequestion: str