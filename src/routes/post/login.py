from typing import Annotated
from typing_extensions import TypedDict
from fastapi import Depends, HTTPException
from server import app, user_repo
from fastapi.security import OAuth2PasswordRequestForm
from src.application.get.login import Login
from src.domain.user.errors.incorrect_password_error import IncorrectPasswordError
from src.domain.user.errors.user_not_found_error import UserNotFoundError
from src.infra.shared.jwt import JWTToken


class TokenContent(TypedDict):
    sub: str
    is_admin: bool


class TokenPayload(TypedDict):
    access_token: str
    token_type: str


@app.post("/jwt")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenPayload:
    try:
        user = Login(user_repo=user_repo).execute(
            form_data.username, form_data.password
        )
    except (UserNotFoundError, IncorrectPasswordError):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    content: TokenContent = {"sub": user.id, "is_admin": user.is_admin}

    return JWTToken(content).value