from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from src.application.get.login import Login
from src.domain.user.errors.incorrect_password_error import IncorrectPasswordError
from src.domain.user.errors.role_not_found_error import RoleNotFoundError
from src.application.create.create_user import CreateUser
from src.domain.user.errors.user_not_found_error import UserNotFoundError
from src.domain.user.user import User
from src.infra.memory_repositories.memory_user_repo import MemoryUserRepo
from src.infra.shared.jwt import JWTToken
from src.infra.storage import Storage


app = FastAPI()
user_repo = MemoryUserRepo(Storage())
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt")


class UserPayload(BaseModel):
    username: str
    password: str
    roles: List[str]


@app.post("/jwt")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = Login().execute(form_data.username, form_data.password)
    except (UserNotFoundError, IncorrectPasswordError):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return JWTToken({"sub": user.id, "is_admin": user.is_admin})


@app.post("/users", status_code=201)
def create_user(
    user_payload: UserPayload, token: Annotated[str, Depends(oauth2_scheme)]
):
    payload = JWTToken.decrypt(token)
    if not payload.get("is_admin"):
        raise HTTPException(status_code=401, detail="Unauthorized.")
    try:
        user_to_create = User(**user_payload.model_dump())
        CreateUser(repo=user_repo, user=user_to_create).execute()
    except RoleNotFoundError:
        raise HTTPException(status_code=400, detail="The role added is not valid.")
