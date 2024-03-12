from dataclasses import dataclass
import datetime
from typing import List
from domain.lead import Lead


@dataclass()
class ECG:
    id: str
    date: datetime.date
    leads: List[Lead]
