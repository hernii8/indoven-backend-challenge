import datetime

import pytest
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.lead import Lead
from src.infra.memory_repositories.memory_ecg_repo import MemoryECGRepository
from src.infra.storage import Storage


@pytest.fixture
def empty_ecg_repo() -> MemoryECGRepository:
    return MemoryECGRepository(Storage())


@pytest.mark.usefixtures("reset_storage")
def test_create_ecg(empty_ecg_repo: MemoryECGRepository):
    """It should create an ECG"""
    ecg = Electrocardiogram(
        id="id",
        date=datetime.datetime.now(),
        lead=[Lead(name="name", signal=[1], n_samples=1)],
    )
    empty_ecg_repo.save(ecg)
    assert len(Storage().ecgs) == 1
    assert Storage().ecgs[0]["id"] == ecg.id
