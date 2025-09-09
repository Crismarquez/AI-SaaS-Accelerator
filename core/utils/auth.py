from __future__ import annotations
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .firebase import verify_id_token


bearer_scheme = HTTPBearer(auto_error=False)


class AuthenticatedUser(Dict[str, Any]):
    """Simple dict-based user model holding Firebase token claims."""


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> AuthenticatedUser:
    if credentials is None or not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    try:
        decoded = verify_id_token(token)
        return AuthenticatedUser(decoded)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


def require_roles(*required_roles: str):
    def dependency(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
        # Expect custom claims in 'roles' as list[str]
        roles = user.get("roles") or user.get("claims", {}).get("roles")
        if required_roles:
            if not isinstance(roles, list) or not any(r in roles for r in required_roles):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return dependency


