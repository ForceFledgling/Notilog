import jwt

from backend.modules.login.schemas import JWTPayload
from backend.settings.config import settings


def create_access_token(*, data: JWTPayload):
    payload = data.model_dump().copy()
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
