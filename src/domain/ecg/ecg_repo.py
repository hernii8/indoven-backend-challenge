from typing import Protocol

from src.domain.ecg.ecg import Electrocardiogram


class ECGRepository(Protocol):
    def save(ecg: Electrocardiogram) -> None:
        pass

    def get(id: str) -> Electrocardiogram:
        pass
