import uvicorn
import os
from fastapi import FastAPI
from src.routes.get.get_metrics import router as get_metrics_router
from src.routes.post.create_ecg import router as create_ecg_router
from src.routes.post.login import router as login_router
from src.routes.post.create_user import router as create_user_router

ENV = os.environ.get("ENV", "development")
tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Electrocardiograms",
        "description": "Operations with electrocardiograms.",
    },
]

app = FastAPI(title="Idoven backend challenge", openapi_tags=tags_metadata)
app.include_router(get_metrics_router, tags=["Users"])
app.include_router(create_ecg_router, tags=["Electrocardiograms"])
app.include_router(create_user_router, tags=["Users"])
app.include_router(login_router, tags=["Users"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
