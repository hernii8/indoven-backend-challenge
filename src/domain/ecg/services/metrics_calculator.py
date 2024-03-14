from dataclasses import dataclass
from typing import List
from src.domain.ecg.ecg import Electrocardiogram


@dataclass
class MetricsCalculator:
    ecg: Electrocardiogram

    def calculate_zero_crossings(self) -> int:
        """Calculates the number of times each ECG channel crosses zero"""
        return sum(
            calculate_zero_crossings_signal(lead.signal) for lead in self.ecg.leads
        )


def calculate_zero_crossings_signal(signal: List[int]) -> int:
    signal_without_zeroes = [number for number in signal if number != 0]
    return sum(
        is_sign_change
        for previous, current in zip(signal_without_zeroes, signal_without_zeroes[1:])
        if (is_sign_change := current * previous < 0)
    )
