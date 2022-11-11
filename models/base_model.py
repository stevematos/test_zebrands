from sqlalchemy.ext.declarative import declarative_base

from config.database import Engine

# Base Entity Model Schema
EntityBase = declarative_base()


def init():
    EntityBase.metadata.create_all(bind=Engine)
