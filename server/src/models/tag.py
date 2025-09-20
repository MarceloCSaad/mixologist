from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from src.models.base_model import BaseModel


class Tag(BaseModel):
    __tablename__ = 'tags'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    cocktail_tag_associations = relationship("CocktailTagAssociation", back_populates="tag", cascade="all, delete-orphan")
    # If you want a convenience property for cocktails, use a property or a viewonly relationship, but do not use back_populates here.

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"
