import time

import jwt
import pytest
from src.infra.jwt.jwt import JWTToken


def test_verify_expiration():
    """It should raise an error if the token has expired"""
    token = JWTToken(
        data={"sub": "id", "is_admin": True}, milliseconds_to_expire=1
    ).access_token
    time.sleep(0.002)
    with pytest.raises(jwt.ExpiredSignatureError):
        JWTToken.decrypt(token)
