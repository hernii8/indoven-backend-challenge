from dataclasses import dataclass
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.ecg_repo import ECGRepository
from src.domain.ecg.services.metrics_calculator import MetricsCalculator
from src.domain.user.errors.unauthorized_error import UnauthorizedError


@dataclass()
class CreateECG:
    repo: ECGRepository
    ecg: Electrocardiogram

    def execute(self, is_admin: bool):
        if is_admin:
            raise UnauthorizedError

        self.ecg.zero_crossings = MetricsCalculator(
            ecg=self.ecg
        ).calculate_zero_crossings()
        self.repo.save(self.ecg)
