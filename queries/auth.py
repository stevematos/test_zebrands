from sqlalchemy.orm import Session

from models.users import Users


def get_user_by_email(db: Session, email: str) -> Users:
    return db.query(Users).filter(Users.email == email).one()
