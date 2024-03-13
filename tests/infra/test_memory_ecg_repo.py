import datetime
from typing import List

import pytest
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.lead import Lead
from src.infra.memory_repositories.memory_ecg_repo import MemoryECGRepository
from src.infra.storage import ECGModel, Storage


@pytest.fixture
def empty_ecg_repo() -> MemoryECGRepository:
    return MemoryECGRepository(Storage())


@pytest.fixture
def loaded_ecg_repo() -> MemoryECGRepository:
    sample_ecgs: List[ECGModel] = [
        {
            "id": "id",
            "date": "01/01/2024 09:00:00",
            "leads": [{"name": "name", "n_samples": 1, "signal": "1,2,3"}],
        }
    ]
    return MemoryECGRepository(Storage(ecgs=sample_ecgs))


@pytest.mark.usefixtures("reset_storage")
def test_create_ecg(empty_ecg_repo: MemoryECGRepository):
    """It should create an ECG"""
    ecg = Electrocardiogram(
        id="id",
        date=datetime.datetime.now(),
        leads=[Lead(name="name", signal=[1], n_samples=1)],
    )
    empty_ecg_repo.save(ecg)
    assert len(Storage().ecgs) == 1
    assert Storage().ecgs[0]["id"] == ecg.id


@pytest.mark.usefixtures("reset_storage")
def test_get_ecg(loaded_ecg_repo: MemoryECGRepository):
    """It should get an ECG by id"""
    expected = Storage().ecgs[0]
    ecg = loaded_ecg_repo.get(expected["id"])
    assert ecg.id == expected["id"]
    assert len(ecg.leads) == 1 and ecg.leads[0].signal == [1, 2, 3]
