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


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


@dataclass(frozen=True)
class Storage(metaclass=Singleton):
    users: List[UserModel] = field(default_factory=lambda: [])

    @classmethod
    def reset(cls):
        cls._instance = None
