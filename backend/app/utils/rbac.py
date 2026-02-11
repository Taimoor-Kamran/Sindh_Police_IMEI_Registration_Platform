from fastapi import Depends, HTTPException

from app.models.user import User
from app.routes.auth import get_current_user


def require_role(*allowed_roles: str):
    """FastAPI dependency that checks the current user has one of the allowed roles."""
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}",
            )
        return current_user
    return dependency


def require_verified_shop(current_user: User = Depends(get_current_user)) -> User:
    """Require the user to be a verified shop keeper."""
    if current_user.role != "shop_keeper":
        raise HTTPException(status_code=403, detail="Access denied. Shop keeper role required")
    if not current_user.is_shop_verified:
        raise HTTPException(status_code=403, detail="Shop keeper account not yet verified by police admin")
    return current_user
