from config.environment import (
    DATABASE_DIALECT,
    DATABASE_HOSTNAME,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USERNAME,
    DEBUG_MODE,
)
from models.base_model import EntityBase
from pydantic import SecretStr
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils.auth import hash_password

if DATABASE_DIALECT == "sqlite":
    DATABASE_URL = f"sqlite:///./{DATABASE_NAME}.db"
else:
    DATABASE_URL = (
        f"{DATABASE_DIALECT}://{DATABASE_USERNAME}:"
        f"{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:"
        f"{DATABASE_PORT}/{DATABASE_NAME}"
    )


# Create Database Engine
Engine = create_engine(DATABASE_URL, echo=DEBUG_MODE, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()


def init():
    import models

    EntityBase.metadata.create_all(bind=Engine)

    db_init = scoped_session(SessionLocal)
    email_admin = "steve.matos.1998@gmail.com"
    user = (
        db_init.query(models.User)
        .filter(models.User.email == email_admin, models.User.is_active)
        .first()
    )
    if not user:
        user = models.User(
            email=email_admin,
            hashed_password=hash_password(SecretStr("test")),
            full_name="Admin",
            rol="admin",
        )

        db_init.add(user)
        db_init.commit()
        db_init.refresh(user)

    db_init.close()
