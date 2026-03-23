from sqlalchemy.orm import Session

from panda_spa.db.models import User
from panda_spa.schema import UserSchema


def create_user(db: Session, user: UserSchema) -> User:
    """
    Create a new user in the database

    :param db: SQLAlchemy session object
    :param user: User data to create
    :return: The newly created user object
    """
    db_user = User(
        name=user.name,
        species=user.species,
        favorite_service_name=user.favorite_service
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
