from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

# Base Entity Model Schema
EntityBase = declarative_base()


class TimestampedBase(EntityBase):
    __abstract__ = True

    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
