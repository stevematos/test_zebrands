from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import Column
from sqlalchemy import DateTime, func

from config.database import Engine

# Base Entity Model Schema
EntityBase = declarative_base()


class TimestampedBase(EntityBase):
    __abstract__ = True

    created_at = Column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
    )


def init():
    import models
    EntityBase.metadata.create_all(bind=Engine)

