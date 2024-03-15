from fastapi import Depends, HTTPException
from src.domain.ecg.errors.metric_not_calculated_error import MetricNotCalculatedError
from src.domain.user.errors.unauthorized_error import UnauthorizedError
from src.routes.dependencies import ecg_repo
from src.application.get.get_metrics import GetMetrics
from src.domain.ecg.errors.ecg_not_found_error import ECGNotFoundError
from src.domain.ecg.errors.not_ecg_owner_error import NotECGOwnerError
from fastapi import APIRouter

from src.routes.middlewares.token_validator import validate_token
from src.routes.post.login import TokenContent

router = APIRouter()


@router.get("/ecgs/{ecg_id}/metrics", status_code=200)
def get_metrics(ecg_id: str, token_content: TokenContent = Depends(validate_token)):
    try:
        zero_crossings = GetMetrics(
            ecg_id=ecg_id, ecg_repo=ecg_repo, user_id=token_content["sub"]
        ).execute(is_admin=token_content["is_admin"])
    except ECGNotFoundError:
        raise HTTPException(status_code=404, detail="Electrocardiogram not found")
    except (NotECGOwnerError, UnauthorizedError):
        raise HTTPException(status_code=401, detail="Unauthorized")
    except MetricNotCalculatedError:
        raise HTTPException(status_code=404, detail="Metric not calculated")

    return {"zero_crossings": zero_crossings}
