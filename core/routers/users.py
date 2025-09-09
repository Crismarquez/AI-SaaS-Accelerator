from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..config import get_db
from .. import schemas
from ..services import user_service
from ..utils.auth import get_current_user, require_roles, AuthenticatedUser


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = user_service.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db, user_in)


@router.get("/me")
def read_me(user: AuthenticatedUser = Depends(get_current_user)):
    # Return minimal profile from token
    return {
        "uid": user.get("uid"),
        "email": user.get("email"),
        "name": user.get("name"),
        "picture": user.get("picture"),
        "roles": user.get("roles") or user.get("claims", {}).get("roles"),
    }


@router.get("/admin/overview")
def admin_overview(user: AuthenticatedUser = Depends(require_roles("admin"))):
    return {"message": "admin ok", "uid": user.get("uid")}


