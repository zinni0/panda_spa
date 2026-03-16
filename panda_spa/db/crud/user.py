from sqlalchemy.orm import Session

from panda_spa.db.models import User
from panda_spa.schema import UserSchema


def create_user(db: Session, user: UserSchema):
    db_user = User(
        name=user.name,
        species=user.species,
        favorite_service_name=user.favorite_service
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
