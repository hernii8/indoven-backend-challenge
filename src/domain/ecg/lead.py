from dataclasses import dataclass, field
from typing import List


@dataclass()
class Lead:
    name: str
    signal: List[int]
    n_samples: int | None = field(default=None)
