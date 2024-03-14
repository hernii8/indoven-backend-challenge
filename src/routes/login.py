from typing import Annotated
from fastapi import Depends, HTTPException
from server import app, user_repo
from fastapi.security import OAuth2PasswordRequestForm
from src.application.get.login import Login
from src.domain.user.errors.incorrect_password_error import IncorrectPasswordError
from src.domain.user.errors.user_not_found_error import UserNotFoundError
from src.infra.shared.jwt import JWTToken


@app.post("/jwt")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = Login(user_repo=user_repo).execute(
            form_data.username, form_data.password
        )
    except (UserNotFoundError, IncorrectPasswordError):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return JWTToken({"sub": user.id, "is_admin": user.is_admin}).value
