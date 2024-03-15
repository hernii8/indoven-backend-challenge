from dataclasses import dataclass
from src.domain.ecg.ecg_repo import ECGRepository
from src.domain.ecg.errors.metric_not_calculated_error import MetricNotCalculatedError
from src.domain.ecg.errors.not_ecg_owner_error import NotECGOwnerError
from src.domain.user.errors.unauthorized_error import UnauthorizedError


@dataclass()
class GetMetrics:
    ecg_repo: ECGRepository
    ecg_id: str
    user_id: str

    def execute(self, is_admin: bool) -> int:
        if is_admin:
            raise UnauthorizedError
        ecg = self.ecg_repo.get(self.ecg_id)
        if self.user_id != ecg.uploader_id:
            raise NotECGOwnerError
        if ecg.zero_crossings is None:
            raise MetricNotCalculatedError
        return ecg.zero_crossings
