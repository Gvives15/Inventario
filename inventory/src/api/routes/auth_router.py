import jwt
from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate
from django.conf import settings
from ninja import Router, Schema
from config.security.jwt_settings import (
    JWT_ALGORITHM,
    JWT_AUDIENCE,
    JWT_ISSUER,
    get_signing_key,
    get_exp_seconds,
)

router = Router()

class TokenIn(Schema):
    username: str
    password: str

class TokenOut(Schema):
    access_token: str
    token_type: str
    expires_in_seconds: int

@router.post("/token", response={200: TokenOut, 401: dict})
def issue_token(request, payload: TokenIn):
    user = authenticate(username=payload.username, password=payload.password)
    if not user or not user.is_active:
        return 401, {"detail": "Invalid credentials"}
    now = datetime.now(timezone.utc)
    exp_seconds = get_exp_seconds()
    claims = {
        "sub": str(user.id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=exp_seconds)).timestamp()),
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
    }
    token = jwt.encode(claims, get_signing_key(settings.SECRET_KEY), algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "Bearer", "expires_in_seconds": exp_seconds}
