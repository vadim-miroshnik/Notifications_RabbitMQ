import time
from typing import Optional, Dict, Any

import jwt
from core.config import settings


def encode_jwt(user_id: str) -> dict[str, str]:
    payload = {"user_id": user_id, "exp": time.time() + 600}
    token = jwt.encode(payload, settings.app.jwt_secret_key, algorithm=settings.app.algorithm)

    return {"access_token": token}


def decode_jwt(token: str) -> Optional[Dict[Any, Any]]:
    try:
        decoded_token = jwt.decode(token, settings.app.jwt_secret_key, algorithms=[settings.app.algorithm])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
