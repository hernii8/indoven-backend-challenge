from datetime import timedelta, timezone, datetime
from jwt import encode, decode

SECRET_KEY = "bba820ebc09747e94a63a99d168932f011b2dccf05ef622080e39e35151332aa"
DEFAULT_ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)
TOKEN_TYPE = "bearer"


class JWTToken:
    __access_token: str
    __token_type: str = TOKEN_TYPE

    def __init__(
        self,
        data: dict,
        minutes_to_expire: timedelta = DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES,
    ):
        to_encode = data.copy()
        expires_in = datetime.now(timezone.utc) + minutes_to_expire
        to_encode.update({"exp": expires_in})
        self.access_token = encode(to_encode, SECRET_KEY, algorithm=DEFAULT_ALGORITHM)

    @staticmethod
    def decrypt(token):
        return decode(token, SECRET_KEY, algorithms=[DEFAULT_ALGORITHM])

    @property
    def access_token(self):
        return self.__access_token

    @access_token.setter
    def access_token(self, value):
        self.__access_token = value
