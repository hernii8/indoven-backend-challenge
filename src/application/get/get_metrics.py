from dataclasses import dataclass
from src.domain.ecg.ecg_repo import ECGRepository
from src.domain.ecg.errors.not_ecg_owner_error import NotECGOwnerError


@dataclass()
class GetMetrics:
    ecg_repo: ECGRepository
    ecg_id: str
    user_id: str

    def execute(self) -> int:
        ecg = self.ecg_repo.get(id)
        if self.user_id != ecg.uploader_id:
            raise NotECGOwnerError
        return ecg.zero_crossings
