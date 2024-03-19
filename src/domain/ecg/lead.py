from dataclasses import dataclass, field
from typing import List


@dataclass()
class Lead:
    name: str
    signal: List[int]
    n_samples: int | None = field(default=None)

    def __post_init__(self):
        if self.n_samples is None:
            self.n_samples = len(self.signal)
