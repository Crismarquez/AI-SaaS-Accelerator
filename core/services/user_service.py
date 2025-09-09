from sqlalchemy.orm import Session
from .. import models, schemas


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    user = models.User(email=user_in.email, full_name=user_in.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


