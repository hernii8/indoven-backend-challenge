from dataclasses import dataclass
import datetime
from typing import List
from src.domain.ecg.lead import Lead


@dataclass()
class Electrocardiogram:
    id: str
    date: datetime.date
    leads: List[Lead]
    zero_crossings: int | None = None
