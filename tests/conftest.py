from typing import Any, Generator
import pytest
from src.infra.storage import Storage


@pytest.fixture()
def reset_storage() -> Generator[None, Any, Any]:
    yield
    Storage.reset()
