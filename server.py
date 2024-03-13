from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel
from src.application.create.create_ecg import CreateECG
from src.application.get.login import Login
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.lead import Lead
from src.domain.user.errors.incorrect_password_error import IncorrectPasswordError
from src.domain.user.errors.role_not_found_error import RoleNotFoundError
from src.application.create.create_user import CreateUser
from src.domain.user.errors.user_not_found_error import UserNotFoundError
from src.domain.user.user import User
from src.infra.memory_repositories.memory_ecg_repo import MemoryECGRepository
from src.infra.memory_repositories.memory_user_repo import MemoryUserRepo
from src.infra.shared.hasher import Hasher
from src.infra.shared.jwt import JWTToken
from src.infra.storage import Storage
from datetime import datetime

app = FastAPI()
user_repo = MemoryUserRepo(
    Storage(
        users=[
            {"username": "username", "password": Hasher.hash("password"), "roles": []},
            {
                "username": "admin",
                "password": Hasher.hash("adminpass"),
                "roles": ["admin"],
            },
        ]
    )
)
ecg_repo = MemoryECGRepository(Storage())
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt")


@app.post("/jwt")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = Login(user_repo=user_repo).execute(
            form_data.username, form_data.password
        )
    except (UserNotFoundError, IncorrectPasswordError):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return JWTToken({"sub": user.id, "is_admin": user.is_admin}).value


class UserPayload(BaseModel):
    username: str
    password: str
    roles: List[str]


@app.post("/users", status_code=201)
def create_user(
    user_payload: UserPayload, token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        payload = JWTToken.decrypt(token)
    except jwt.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")
    if not payload.get("is_admin"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        user_to_create = User(**user_payload.model_dump())
        CreateUser(repo=user_repo, user=user_to_create).execute()
    except RoleNotFoundError:
        raise HTTPException(status_code=400, detail="The role added is not valid")


class LeadPayload(BaseModel):
    name: str
    signal: List[int]
    # Not required
    n_samples: int


class ECGPayload(BaseModel):
    id: str
    date: str
    leads: List[LeadPayload]


@app.post("/ecgs", status_code=201)
def create_ecg(ecg_payload: ECGPayload, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = JWTToken.decrypt(token)
    except jwt.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")
    if payload.get("is_admin"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    # TODO: Refactor this!
    ecg_payload.date = datetime.strptime(ecg_payload.date, "%d/%m/%Y %H:%M:%S")
    ecg_payload.leads = [
        Lead(name=lead.name, signal=lead.signal, n_samples=lead.n_samples)
        for lead in ecg_payload.leads
    ]
    ######
    ecg_to_create = Electrocardiogram(
        id=ecg_payload.id, date=ecg_payload.date, leads=ecg_payload.leads
    )
    CreateECG(repo=ecg_repo, ecg=ecg_to_create).execute()
