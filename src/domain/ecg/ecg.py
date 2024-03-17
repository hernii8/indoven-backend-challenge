from dataclasses import dataclass
from datetime import datetime
from typing import List
from src.domain.ecg.lead import Lead


@dataclass()
class Electrocardiogram:
    id: str
    date: datetime
    leads: List[Lead]
    uploader_id: str
    zero_crossings: int | None = None
