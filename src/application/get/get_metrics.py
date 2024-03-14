from dataclasses import dataclass

from src.domain.ecg.ecg_repo import ECGRepository


@dataclass()
class GetMetrics:
    ecg_repo: ECGRepository
    ecg_id: str

    def execute(self) -> int:
        ecg = self.ecg_repo.get(id)
        return ecg.zero_crossings
