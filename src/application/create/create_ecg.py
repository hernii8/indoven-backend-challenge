from dataclasses import dataclass
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.ecg_repo import ECGRepository


@dataclass()
class CreateECG:
    repo: ECGRepository
    ecg: Electrocardiogram

    def execute(self):
        self.repo.save(self.ecg)
