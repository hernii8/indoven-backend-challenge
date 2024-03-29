from dataclasses import dataclass, field
from typing import List, TypedDict

"""This is just a fake implementation of what could be a database or another storage type.
The selects/creates/updates will be done directly in the lists to avoid queries, the models are also created to give realism.
The storage would be treated as a connection dependency in the repositories."""


class UserModel(TypedDict):
    id: str
    username: str
    password: str
    roles: List[str]


class LeadModel(TypedDict):
    name: str
    n_samples: int | None
    signal: str


class ECGModel(TypedDict):
    id: str
    date: str
    leads: List[LeadModel]
    zero_crossings: int | None
    uploader_id: str


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


@dataclass(frozen=True)
class Storage(metaclass=Singleton):
    users: List[UserModel] = field(default_factory=list)
    ecgs: List[ECGModel] = field(default_factory=list)

    @classmethod
    def reset(cls):
        cls._instance = None
