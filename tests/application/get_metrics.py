import pytest
from src.application.get.get_metrics import GetMetrics
from src.domain.ecg.errors.not_ecg_owner_error import NotECGOwnerError
from src.infra.memory_repositories.memory_ecg_repo import MemoryECGRepository
from src.infra.storage import Storage


def test_not_uploader_error():
    """It should raise an error if the user requesting the metrics is not the uploader of the ECG"""
    with pytest.raises(NotECGOwnerError):
        GetMetrics(MemoryECGRepository(Storage()), "uploader_id", "not_uploader_id")
