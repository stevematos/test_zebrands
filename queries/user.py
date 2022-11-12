from sqlalchemy.orm import Session

from models.users import User


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).one()


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, _id: int, user: User) -> User:
    user.id = _id
    db.merge(user)
    db.commit()
    return user


def delete_user(db: Session, _id: int):
    db.query(User).filter(User.id == _id).update({'is_active': False})
    db.commit()
