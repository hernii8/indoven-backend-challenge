import uvicorn
import os
from fastapi import FastAPI
from src.routes.get.get_metrics import router as get_metrics_router
from src.routes.post.create_ecg import router as create_ecg_router
from src.routes.post.login import router as login_router
from src.routes.post.create_user import router as create_user_router

ENV = os.environ.get("ENV", "development")
app = FastAPI()
app.include_router(get_metrics_router)
app.include_router(create_ecg_router)
app.include_router(create_user_router)
app.include_router(login_router)

if __name__ == "__main__":
    uvicorn.run(app)
