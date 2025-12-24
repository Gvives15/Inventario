import os
from datetime import timedelta

JWT_TTL = int(os.getenv("JWT_TTL_SECONDS", 43200))
JWT_ISSUER = os.getenv("JWT_ISSUER", "inventario-v1")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "inventario-api")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY", None)

def get_signing_key(default_secret: str) -> str:
    return JWT_SIGNING_KEY or default_secret

def get_exp_seconds() -> int:
    return JWT_TTL
