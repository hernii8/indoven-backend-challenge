from typing import Annotated
from fastapi import Depends, HTTPException
import jwt
from src.infra.shared.jwt import JWTToken
from src.routes.dependencies import oauth2_scheme
from src.routes.post.login import TokenContent


def validate_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenContent:
    try:
        content: TokenContent = JWTToken.decrypt(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.DecodeError, jwt.InvalidTokenError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid token")

    return content
