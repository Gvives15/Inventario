import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja.security import HttpBearer
from datetime import datetime, timezone
from config.security.jwt_settings import JWT_ALGORITHM, JWT_AUDIENCE, JWT_ISSUER, get_signing_key

User = get_user_model()

class JWTBearer(HttpBearer):
    def authenticate(self, request, token: str):
        key = get_signing_key(settings.SECRET_KEY)
        data = jwt.decode(
            token,
            key,
            algorithms=[JWT_ALGORITHM],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
        )
        uid = data.get("sub")
        if not uid:
            return None
        try:
            user = User.objects.get(id=uid, is_active=True)
        except User.DoesNotExist:
            return None
        request.user = user
        return user
