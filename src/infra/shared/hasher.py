from passlib.context import CryptContext


class Hasher:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, plain: str) -> str:
        return cls.pwd_context.hash(plain)

    @classmethod
    def verify(cls, plain: str, hash: str) -> bool:
        return cls.pwd_context.verify(plain, hash)
