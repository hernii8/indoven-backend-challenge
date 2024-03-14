from typing import Annotated
from fastapi import Depends, HTTPException
import jwt
from server import app, oauth2_scheme, ecg_repo
from src.application.get.get_metrics import GetMetrics
from src.domain.ecg.errors.ecg_not_found_error import ECGNotFoundError
from src.domain.ecg.errors.not_ecg_owner_error import NotECGOwnerError
from src.infra.shared.jwt import JWTToken


@app.get("/ecgs/{ecg_id}/metrics", status_code=200)
def get_metrics(ecg_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = JWTToken.decrypt(token)
    except jwt.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")
    if payload.get("is_admin"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        zero_crossings = GetMetrics(ecg_id=ecg_id, ecg_repo=ecg_repo).execute()
    except ECGNotFoundError:
        raise HTTPException(status_code=404, detail="Electrocardiogram not found")
    except NotECGOwnerError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"zero_crossings": zero_crossings}
