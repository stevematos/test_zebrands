from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config.environment import config_env

# Runtime Environment Configuration
env = config_env()

# Generate Database URL
if env.DATABASE_DIALECT == "sqlite":
    DATABASE_URL = f"sqlite:///./{env.DATABASE_NAME}.db"
else:
    DATABASE_URL = f"{env.DATABASE_DIALECT}://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}@{env.DATABASE_HOSTNAME}:{env.DATABASE_PORT}/{env.DATABASE_NAME}"

# Create Database Engine
Engine = create_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
