from datetime import datetime
from typing import List, Optional
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from server import app, ecg_repo
from src.application.create.create_ecg import CreateECG
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.lead import Lead
from src.routes.middlewares.token_validator import validate_token
from src.routes.post.login import TokenContent


class CreateLeadPayload(BaseModel):
    name: str
    signal: List[int]
    n_samples: Optional[int]


class CreateECGPayload(BaseModel):
    id: str
    date: str
    leads: List[CreateLeadPayload]


@app.post("/ecgs", status_code=201)
def create_ecg(
    ecg_payload: CreateECGPayload, token_content: TokenContent = Depends(validate_token)
):
    if token_content["is_admin"]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    ecg_to_create = ecg_payload_to_ecg(ecg_payload, token_content["sub"])
    CreateECG(repo=ecg_repo, ecg=ecg_to_create).execute()


def ecg_payload_to_ecg(payload: CreateECGPayload, user_id: str) -> Electrocardiogram:
    return Electrocardiogram(
        id=payload.id,
        date=datetime.strptime(payload.date, "%d/%m/%Y %H:%M:%S"),
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
