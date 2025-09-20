from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from measured import Volume, Mass
from measured import Unit

from src.models.base_model import BaseModel


class Ingredient(BaseModel):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(124), unique=True, index=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Ingredient(name={self.name})>"

