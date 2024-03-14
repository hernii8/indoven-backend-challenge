from datetime import datetime
import pytest
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.lead import Lead
from src.domain.ecg.services.metrics_calculator import MetricsCalculator


@pytest.mark.parametrize(
    "signal_sut, expected",
    [
        ([0, 0, 0], 0),
        ([1, 1, 1], 0),
        ([-1, -1, -1], 0),
        ([-1, 1], 1),
        ([1, -1], 1),
        ([-1, 0, 1], 1),
        ([1, 0, -1], 1),
        ([1, 0, -1, 0, 1, 0, 1, 0, 0, -999], 3),
    ],
)
def test_crossing_zeroes_calculation(signal_sut, expected):
    ecg = Electrocardiogram(
        id="id",
        date=datetime.now(),
        leads=[Lead(name="name", signal=signal_sut)],
        uploader_id="u_id",
    )
    """It should return the number of times a lead crosses zero, by combining the zero crossings of all its signals"""
    assert MetricsCalculator(ecg=ecg).calculate_zero_crossings() == expected
