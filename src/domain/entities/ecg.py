from dataclasses import dataclass
import datetime
from typing import List
from src.domain.value_objects.lead import Lead


@dataclass()
class Electrocardiogram:
    id: str
    date: datetime.date
    leads: List[Lead]
