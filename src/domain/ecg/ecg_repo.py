from typing import List, Protocol

from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.lead import Lead


class ECGRepository(Protocol):
    def save(self, ecg: Electrocardiogram) -> None:
        pass

    def get(self, id: str) -> Electrocardiogram:
        pass

    def calculate_zero_crosses(self, leads: List[Lead]) -> int:
        pass
