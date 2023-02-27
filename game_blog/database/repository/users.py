from sqlalchemy.orm import Session

from game_blog.core.hashing import Hasher
from game_blog.apps.authapp.models import User
from game_blog.apps.authapp.schemas import UserCreate


def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
