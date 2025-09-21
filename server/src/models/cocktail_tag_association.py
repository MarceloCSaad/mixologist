from typing import Optional
from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base_model import BaseModel


class CocktailTagAssociation(BaseModel):
    __tablename__ = "cocktail_tag_association"
    cocktail_id = Column(Integer, ForeignKey("cocktails.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    # Relationships
    cocktail = relationship("Cocktail", back_populates="cocktail_tag_associations")
    tag = relationship("Tag", back_populates="cocktail_tag_associations")

    def __init__(self, cocktail_id: Optional[int] = None, tag_id: Optional[int] = None):
        self.cocktail_id = cocktail_id
        self.tag_id = tag_id
