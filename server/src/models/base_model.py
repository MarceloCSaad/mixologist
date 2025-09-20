from sqlalchemy.orm import DeclarativeBase

from src.database.db_service import DBModel


class BaseModel(DeclarativeBase, DBModel):
    """Base class for all ORM models."""
    pass
