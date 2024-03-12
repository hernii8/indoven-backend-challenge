from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Lead:
    name: str
    n_samples: int | None
    signal: List[int]
