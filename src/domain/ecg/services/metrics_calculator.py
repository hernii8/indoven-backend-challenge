from dataclasses import dataclass
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.ecg_repo import ECGRepository


@dataclass
class MetricsCalculator:
    ecg_repo: ECGRepository
    ecg: Electrocardiogram

    def calculate_zero_crosses(self) -> int:
        """Calculates the number of times each ECG channel crosses zero"""
        return self.ecg_repo.calculate_zero_crosses(self.ecg.leads)
