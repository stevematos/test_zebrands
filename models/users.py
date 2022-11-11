from models.base_model import EntityBase

from sqlalchemy import Column
from sqlalchemy import Integer, String


class Users(EntityBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    hashed_password = Column(String(255))

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
        }
