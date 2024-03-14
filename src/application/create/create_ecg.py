from dataclasses import dataclass
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.ecg_repo import ECGRepository
from src.domain.ecg.services.metrics_calculator import MetricsCalculator


@dataclass()
class CreateECG:
    repo: ECGRepository
    ecg: Electrocardiogram

    def execute(self):
        self.ecg.zero_crossings = MetricsCalculator(
            ecg=self.ecg, ecg_repo=self.repo
        ).calculate_zero_crosses()
        self.repo.save(self.ecg)
