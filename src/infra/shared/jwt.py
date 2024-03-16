from datetime import timedelta, timezone, datetime
from typing import Any, cast
from jwt import encode, decode

SECRET_KEY = "bba820ebc09747e94a63a99d168932f011b2dccf05ef622080e39e35151332aa"
DEFAULT_ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MILLISECONDS = 8.64e7  # 1 day
TOKEN_TYPE = "bearer"


class JWTToken:
    __access_token: str
    __token_type: str = TOKEN_TYPE

    def __init__(
        self,
        data: dict,
        milliseconds_to_expire: float = DEFAULT_ACCESS_TOKEN_EXPIRE_MILLISECONDS,
    ):
        to_encode = data.copy()
        expires_in = datetime.now(timezone.utc) + timedelta(
            milliseconds=milliseconds_to_expire
        )
        to_encode.update({"exp": expires_in})
        self.access_token = encode(
            cast(dict[str, Any], to_encode), SECRET_KEY, algorithm=DEFAULT_ALGORITHM
        )

    @staticmethod
    def decrypt(token):
        return decode(
            token,
            SECRET_KEY,
            algorithms=[DEFAULT_ALGORITHM],
            options={"verify_signature": True, "verify_exp": True},
        )

    @property
    def access_token(self):
        return self.__access_token

    @access_token.setter
    def access_token(self, value):
        self.__access_token = value

    @property
    def value(self):
        return {"access_token": self.access_token, "token_type": self.__token_type}
