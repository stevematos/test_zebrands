from models.base_model import EntityBase

from sqlalchemy import Column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import Enum as SQAEnum

from config.constants import RolEnum


class User(EntityBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    rol = Column(SQAEnum(RolEnum))
    is_active = Column(Boolean, default=True)
