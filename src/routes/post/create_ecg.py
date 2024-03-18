from typing import List, Optional
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from src.domain.user.errors.unauthorized_error import UnauthorizedError
from src.routes.dependencies import ecg_repo
from src.application.create.create_ecg import CreateECG
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.lead import Lead
from src.routes.middlewares.token_validator import validate_token
from src.routes.post.login import TokenContent
from fastapi import APIRouter

from utils.date_converter import InvalidDateError, str_to_date

router = APIRouter()


class CreateLeadPayload(BaseModel):
    name: str
    signal: List[int]
    n_samples: Optional[int]


class CreateECGPayload(BaseModel):
    id: str
    date: str
    leads: List[CreateLeadPayload]


@router.post(
    "/ecgs",
    status_code=201,
    responses={
        400: {"description": "Invalid date format"},
        401: {"description": "Unauthorized"},
    },
)
def create_ecg(
    ecg_payload: CreateECGPayload, token_content: TokenContent = Depends(validate_token)
):
    """Create an Electrocardiogram"""
    try:
        ecg_to_create = ecg_payload_to_ecg(ecg_payload, token_content["sub"])
        CreateECG(repo=ecg_repo, ecg=ecg_to_create).execute(
            is_admin=token_content["is_admin"]
        )
    except UnauthorizedError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except InvalidDateError:
        print("EXCEPT")
        raise HTTPException(status_code=400, detail="Invalid date format")


def ecg_payload_to_ecg(payload: CreateECGPayload, user_id: str) -> Electrocardiogram:
    return Electrocardiogram(
        id=payload.id,
        date=str_to_date(payload.date),
        leads=[
            Lead(
                name=lead.name,
                signal=lead.signal,
                n_samples=lead.n_samples if hasattr(lead, "n_samples") else None,
            )
            for lead in payload.leads
        ],
        uploader_id=user_id,
    )
