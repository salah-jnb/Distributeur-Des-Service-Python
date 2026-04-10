from dataclasses import dataclass
from datetime import datetime

@dataclass
class Conversation:
    id: int
    question: str
    date: datetime
    typedequestion: str
    personne: str