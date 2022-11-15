from config.constants import RolEnum
from models.base_model import TimestampedBase
from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SQAEnum
from sqlalchemy import Integer, String


class User(TimestampedBase):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(255), index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    rol = Column(SQAEnum(RolEnum))
    is_active = Column(Boolean, default=True)
