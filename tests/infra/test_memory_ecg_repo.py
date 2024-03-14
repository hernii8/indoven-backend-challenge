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
            "zero_crossings": 1,
        }
    ]
    return MemoryECGRepository(Storage(ecgs=sample_ecgs))


@pytest.mark.usefixtures("reset_storage")
def test_create_ecg(empty_ecg_repo: MemoryECGRepository):
    """It should create an ECG"""
    expected_date = "01/01/2024 09:00:00"
    expected_ecg = Electrocardiogram(
        id="id",
        date=datetime.datetime.strptime(expected_date, "%d/%m/%Y %H:%M:%S"),
        leads=[Lead(name="name", signal=[1, 2], n_samples=1)],
    )
    empty_ecg_repo.save(expected_ecg)
    sut_ecg = Storage().ecgs[0]
    assert len(Storage().ecgs) == 1
    assert sut_ecg["id"] == expected_ecg.id
    assert sut_ecg["date"] == expected_date
    assert sut_ecg["leads"][0]["name"] == "name"
    assert sut_ecg["leads"][0]["signal"] == "1,2"
    assert sut_ecg["leads"][0]["n_samples"] == 1


@pytest.mark.usefixtures("reset_storage")
def test_get_ecg(loaded_ecg_repo: MemoryECGRepository):
    """It should get an ECG by id"""
    expected_date = "01/01/2024 09:00:00"
    expected = Storage().ecgs[0]
    sut_ecg = loaded_ecg_repo.get(expected["id"])

    assert sut_ecg.id == expected["id"]
    assert sut_ecg.date == datetime.datetime.strptime(
        expected_date, "%d/%m/%Y %H:%M:%S"
    )
    assert len(sut_ecg.leads) == 1
    assert sut_ecg.leads[0].name == "name"
    assert sut_ecg.leads[0].n_samples == 1
    assert sut_ecg.leads[0].signal == [1, 2, 3]
