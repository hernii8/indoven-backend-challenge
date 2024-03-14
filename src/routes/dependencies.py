from fastapi.security import OAuth2PasswordBearer
from src.infra.memory_repositories.memory_ecg_repo import MemoryECGRepository
from src.infra.memory_repositories.memory_user_repo import MemoryUserRepo
from src.infra.storage import Storage

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt")
user_repo = MemoryUserRepo(Storage())
ecg_repo = MemoryECGRepository(Storage())
