from typing import List, Optional
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel
from src.models.cocktail_tag_association import CocktailTagAssociation
from src.models.constants import CocktailGlassware
from src.models.step import Step
from src.models.tag import Tag


class Cocktail(BaseModel):
    __tablename__ = 'cocktails'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    glassware: Mapped[CocktailGlassware] = mapped_column(Enum(CocktailGlassware), nullable=False, default=CocktailGlassware.LOWBALL)
    # ORM relationship for all steps (bidirectional, for ORM integrity)
    all_steps = relationship(
        "Step",
        back_populates="cocktail",
        cascade="all, delete-orphan"
    )
    cocktail_tag_associations: Mapped[List[CocktailTagAssociation]]  = relationship("CocktailTagAssociation", back_populates="cocktail", cascade="all, delete-orphan")

    def __init__(self, name: str, description: Optional[str] = None, glassware: Optional[CocktailGlassware] = None) -> None:
        self.name = name
        self.description = description
        self.glassware = glassware

    def __repr__(self) -> str:
        return f"<Cocktail(id={self.id}, name={self.name}, total steps={len(self.steps)})>"

    @property
    def first_step(self) -> Optional['Step']:
        return next((s for s in self.all_steps if s.is_recipe_first_step), None)

    @property
    def steps(self) -> List['Step']:
        """
        Returns the steps of the cocktail in order, starting from the first step.
        """
        steps = []
        current_step = self.first_step
        while current_step:
            steps.append(current_step)
            current_step = current_step.next_step
        return steps


    @property
    def tags(self) -> List[Tag]:
        """
        Returns a list of Tag objects associated with this cocktail.
        """
        return [assoc.tag for assoc in self.cocktail_tag_associations if assoc.tag]

    @property
    def total_steps(self) -> int:
        return len(self.steps)

    @property
    def last_step(self) -> Optional[Step]:
        return self.steps[-1] if self.steps else None

    def get_human_readable_glassware(self) -> str:
        """
        Returns a human-readable string for the glassware type.
        """
        glassware = self.glassware.value if self.glassware and hasattr(self.glassware, 'value') else str(self.glassware)
        return glassware.replace('_', ' ').lower().strip()

    def get_human_readable_instructions(self) -> str:
        """
        Returns a human-readable string of the cocktail's recipe instructions.
        """
        instructions = []
        for i, step in enumerate(self.steps):
            step_instruction = f"Step {i + 1}: " + step.get_human_readable_step_explanation()
            if ":glassware" in step_instruction:
                glassware_name = self.get_human_readable_glassware()
                step_instruction = step_instruction.replace(":glassware", glassware_name)
            instructions.append(step_instruction)
        return "\n".join(instructions)
