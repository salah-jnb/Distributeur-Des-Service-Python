from dataclasses import dataclass
@dataclass
class InformationPersonelle:
    id: int
    question: str
    reponce: str
    date: str
    acteur: str
    typedequestion: str