import re

from typing import Optional
from sqlalchemy import Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from src.helpers.number_helper import measured_ingredient_to_pluralized_string, pluralize_word
from src.models.base_model import BaseModel
from src.models.constants import ActionToHumanReadableMapper, MeasuringUnit, MixologyTool, StepAction
from src.models.ingredient import Ingredient


class Step(BaseModel):
    __tablename__ = 'steps'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action: Mapped[StepAction] = mapped_column(Enum(StepAction), nullable=False)
    ingredient_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ingredients.id"), nullable=True)
    measuring_unit: Mapped[Optional[MeasuringUnit]] = mapped_column(Enum(MeasuringUnit), nullable=True)
    quantity: Mapped[Optional[Float]] = mapped_column(Float, nullable=True)
    mixology_tool: Mapped[Optional[MixologyTool]] = mapped_column(Enum(MixologyTool), nullable=True)
    next_step_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("steps.id", ondelete="CASCADE"), nullable=True)
    next_step: Mapped[Optional['Step']] = relationship(
        "Step",
        remote_side=[id],
        cascade="all, delete-orphan",
        single_parent=True
    )
    is_recipe_first_step: Mapped[bool] = mapped_column(default=False, nullable=False)

    cocktail_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("cocktails.id", ondelete="CASCADE"), nullable=True)
    cocktail = relationship("Cocktail", back_populates="all_steps")

    ingredient = relationship("Ingredient")

    def __init__(
        self,
        action: StepAction,
        ingredient: Optional[Ingredient] = None,
        measuring_unit: Optional[str] = None,
        quantity: Optional[float] = None,
        next_step: Optional['Step'] = None
    ):
        self.action = action
        self.ingredient = ingredient
        self.measuring_unit = measuring_unit
        self.quantity = quantity
        self.next_step = next_step

    def __repr__(self):
        return f"<Step(id={self.id}, action={self.action.value}, next_step={self.next_step.id if self.next_step else None})>"


    @staticmethod
    def validate_first_step_uniqueness(session, cocktail_id):
        """
        Validates that only one step per cocktail has is_recipe_first_step=True.
        Raises ValueError if more than one is found.
        """
        from sqlalchemy import select
        from src.models.step import Step
        q = select(Step).where(Step.cocktail_id == cocktail_id, Step.is_recipe_first_step == True)
        results = session.execute(q).scalars().all()
        if len(results) > 1:
            raise ValueError(f"Cocktail {cocktail_id} has multiple first steps.")

    @staticmethod
    def validate_linked_list_integrity(session, cocktail_id):
        """
        Validates that the steps for a cocktail form a valid linked list (no cycles, all reachable).
        Raises ValueError if a cycle or orphan is detected.
        """
        from sqlalchemy import select
        from src.models.step import Step
        steps = session.execute(select(Step).where(Step.cocktail_id == cocktail_id)).scalars().all()
        seen = set()
        first_steps = [s for s in steps if s.is_recipe_first_step]
        if not first_steps:
            return  # No steps, nothing to check
        current = first_steps[0]
        while current:
            if current.id in seen:
                raise ValueError(f"Cycle detected in steps for cocktail {cocktail_id}.")
            seen.add(current.id)
            current = current.next_step
        all_ids = set(s.id for s in steps)
        orphan_ids = all_ids - seen
        if orphan_ids:
            print(f"{orphan_ids} Orphan {pluralize_word('step') if len(orphan_ids) != 1 else 'step'} for cocktail_id=({cocktail_id}): {orphan_ids}")
            raise ValueError(f"Orphan steps detected for cocktail {cocktail_id}: {orphan_ids}")

    def get_human_readable_measured_ingredient(self) -> str:
        """
        Returns a human-readable string representing the measured ingredient.
        If no quantity is provided, it returns just the ingredient name.
        If the ingredient is missing, it returns "ingredient".
        If quantity is provided without measuring unit, it returns "<quantity> <ingredient>".
        
        Examples:
            "50 ml of vodka"
            "1 dash of angostura"
            "2 cubes of ice"
            "straw"
        """
        if not self.ingredient or not self.ingredient.name:
            return "ingredient"

        return measured_ingredient_to_pluralized_string(
            ingredient_name=self.ingredient.name,
            measuring_unit=self.measuring_unit,
            quantity=self.quantity,
        )

    def get_human_readable_step_explanation(self) -> str:
        """
        Returns a human-readable explanation of the step, replacing placeholders with actual values.
        Placeholders:
            - :ingredient -> replaced with the measured ingredient (e.g., "50 ml of vodka")
            - :object -> replaced with the mixology tool (e.g., "shaker")
            - :glassware -> NOT replaced, instead passed forward to Recipe at the linked list Head (Recipe class knows the glassware)
        """
        explanation = ActionToHumanReadableMapper.get(self.action, self.action.value)
        if ":ingredient" in explanation:
            human_readable_ingredient = self.get_human_readable_measured_ingredient()
            explanation = explanation.replace(":ingredient", human_readable_ingredient)
        if ":object" in explanation:
            object_name = self.mixology_tool.value if self.mixology_tool else "object"
            explanation = explanation.replace(":object", object_name)
        
        # Replace underscores with spaces, then remove extra spaces and trim trailing spaces
        explanation = re.sub(' +', ' ', explanation.replace('_', ' ').lower()).strip()
        return explanation.capitalize()
