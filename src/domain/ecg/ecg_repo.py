from typing import Protocol

from src.domain.ecg.ecg import Electrocardiogram


class ECGRepository(Protocol):
    def save(self, ecg: Electrocardiogram) -> None:
        pass

    def get(self, id: str) -> Electrocardiogram:
        pass
