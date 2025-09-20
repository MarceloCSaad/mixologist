from typing import List, Optional
from sqlalchemy.orm import Session

from src.database.db_service import PGDatabaseService
from src.database.session_decorator import with_upper_scope_session
from src.models.constants import MeasuringUnit, StepAction
from src.models.cocktail import Cocktail
from src.models.cocktail_tag_association import CocktailTagAssociation
from src.models.ingredient import Ingredient
from src.models.step import Step
from src.models.tag import Tag


class CocktailService(PGDatabaseService):
    """
    Service to manage Cocktail-related database operations.
    """
    def __init__(self):
        super().__init__()

    def _validate_recipe_integrity(self, session: Session, cocktail: Cocktail):
        """
        Validates that the cocktail's recipe linked list is well-formed and has a unique head.
        """
        Step.validate_first_step_uniqueness(session, cocktail.id)
        Step.validate_linked_list_integrity(session, cocktail.id)

    def _get_filter_conditions(self, id: Optional[int] = None, name: Optional[str] = None, tags: Optional[List[Tag]] = None, ingredients: Optional[List[Ingredient]] = None):
        filter_conditions = []
        if id:
            filter_conditions.append(Cocktail.id == id)
        if name:
            filter_conditions.append(Cocktail.name == name)
        if tags:
            filter_conditions.append(Cocktail.cocktail_tag_associations.any(CocktailTagAssociation.tag_id.in_([tag.id for tag in tags])))
        if ingredients:
            for ingredient in ingredients:
                filter_conditions.append(Cocktail.all_steps.any(Step.ingredient_id == ingredient.id))
        return filter_conditions

    @with_upper_scope_session
    def fetch_cocktails(self, id: Optional[int], name: Optional[str], tags: Optional[List[Tag]] = [], with_ingredients: Optional[List[Ingredient]] = None, session: Session = None) -> List[Cocktail]:
        """
        Fetches cocktails from the database based on optional filters: id, name, and tags.
        If no filters are provided, all cocktails are returned.
        """
        cocktails = session.query(Cocktail).filter_by(*self._get_filter_conditions(id=id, name=name, tags=tags, ingredients=with_ingredients)).all()
        return list(cocktails)

    @with_upper_scope_session
    def update_or_create(self, name: str, description: str, tags: Optional[List[Tag]] = [], steps: Optional[List[Step]] = [], validate: Optional[bool] = True, session: Session = None) -> Cocktail:
        """
        Updates an existing cocktail if one with the same name exists, otherwise creates a new cocktail.
        Uses create_step_linked_list to set up the linked list and cocktail references.
        """
        existing_cocktail = session.query(Cocktail).filter_by(name=name).first()
        if existing_cocktail:
            existing_cocktail.description = description
            # Remove old steps by deleting the head (cascades to all steps)
            old_head = existing_cocktail.first_step
            if old_head:
                session.delete(old_head)
                session.flush()
                existing_cocktail.all_steps.clear()
            self.create_step_linked_list(session=session, steps=steps, cocktail=existing_cocktail, validate=validate)
            existing_cocktail = self.associate_tags_with_cocktail(existing_cocktail, tags or [], session=session)
            return existing_cocktail
        new_cocktail = Cocktail(name=name, description=description)
        session.add(new_cocktail)
        self.create_step_linked_list(session=session, steps=steps, cocktail=new_cocktail, validate=validate)
        return new_cocktail

    @with_upper_scope_session
    def delete_cocktail(self, cocktail_id: int, session: Session = None) -> bool:
        """
        Safely deletes a cocktail and all its steps and tag associations.
        Does NOT delete tags or ingredients.
        Returns True if deleted, False if not found.
        """
        cocktail = session.query(Cocktail).filter_by(id=cocktail_id).first()
        if not cocktail:
            return False

        for step in list(cocktail.all_steps):
            session.delete(step)

        for assoc in list(cocktail.cocktail_tag_associations):
            session.delete(assoc)

        session.delete(cocktail)
        session.flush()
        return True

    @with_upper_scope_session
    def remove_step_from_recipe(self, cocktail: Cocktail, step_id: int, validate: Optional[bool] = True, session: Session = None) -> bool:
        """
        Removes a step from a cocktail's recipe linked list, relinking adjacent nodes as needed.
        Returns True if removed, False if not found.
        """
        steps = cocktail.steps
        if not steps:
            return False
        step_to_remove = next((s for s in steps if s.id == step_id), None)
        if not step_to_remove:
            return False

        if step_to_remove.is_recipe_first_step:
            next_step = step_to_remove.next_step
            if next_step:
                next_step.is_recipe_first_step = True
            session.delete(step_to_remove)
            if validate:
                self._validate_recipe_integrity(session, cocktail)
            session.flush()
            return True

        prev = None
        for s in steps:
            if s.next_step and s.next_step.id == step_id:
                prev = s
                break
        if prev:
            prev.next_step = step_to_remove.next_step
        session.delete(step_to_remove)
        if validate:
            self._validate_recipe_integrity(session, cocktail)
        session.flush()
        return True

    @with_upper_scope_session
    def clear_all_recipe_steps(self, cocktail: Cocktail, session: Session = None) -> None:
        """
        Removes all steps from a cocktail's recipe.
        """
        for step in list(cocktail.all_steps):
            session.delete(step)
        session.flush()

    @with_upper_scope_session
    def create_step(
        self,
        cocktail: Cocktail,
        action: StepAction,
        ingredient: Optional[Ingredient] = None,
        measuring_unit: Optional[MeasuringUnit] = None,
        quantity: Optional[float] = None,
        session: Session = None,
    ) -> Step:
        """
        Create a new cocktail preparation Step, always linked to a cocktail.
        The Step still needs to be linked into the cocktail's linked list of steps separately.
        """
        step = Step(
            action=action,
            ingredient=ingredient,
            measuring_unit=measuring_unit,
            quantity=quantity,
            cocktail=cocktail
        )

        # Commits after mutation and refreshes the new step.
        session.add(step)
        session.commit()
        session.refresh(step)
        return step

    @with_upper_scope_session
    def create_step_linked_list(self, steps: List[Step], cocktail: Cocktail, validate: Optional[bool] = True, session: Session = None) -> Cocktail:
        """
        Sets up a linked list of Steps for a given cocktail.
        The head will be the first step from the provided list, each pointing to the next.
        Sets is_recipe_first_step=True for the head, False for others.
        """
        if not steps:
            return cocktail

        # Link in reverse order: last step points to None, each previous points to the next
        next_step = None
        for i in reversed(range(len(steps))):
            step = steps[i]
            step.cocktail = cocktail
            step.next_step = next_step
            step.is_recipe_first_step = (i == 0)
            session.add(step)
            next_step = step
        if validate:
            self._validate_recipe_integrity(session, cocktail)
        session.flush()
        return cocktail
    
    @with_upper_scope_session
    def add_step_to_specific_recipe_position(self, new_step: Step, recipe_step_order: Optional[int] = None, validate: Optional[bool] = True, session: Session = None) -> Cocktail:
        """
        Insert a new step at a specific position in a cocktail's recipe (1-based).
        - 1 means insert as the new first step.
        - If no steps or index < 1, inserts at head.
        - If index > length, appends at tail.
        - Otherwise, shifts current and later steps right.
        """
        cocktail = new_step.cocktail
        session.refresh(cocktail)
        steps = cocktail.steps

        list_index = recipe_step_order - 1 if recipe_step_order and recipe_step_order > 0 else None

        # Insert at head if recipe is empty (no steps) or list_index is less than 1. A list_index of None should instead be inserted at tail.
        if not steps or (list_index and list_index < 1):
            return self.insert_step_to_recipe_head(new_step, session)

        # Append at tail if no index provided, or if index is greater than length
        if list_index is None or list_index > len(steps):
            return self.append_step_to_end_of_recipe(new_step, session)

        # Insert in the middle (at list_index, shifting current and after right)
        prev = steps[list_index - 1] if list_index > 0 else None
        current = steps[list_index]
        new_step.next_step = current
        new_step.is_recipe_first_step = False
        if prev:
            prev.next_step = new_step
        if validate:
            self._validate_recipe_integrity(session, cocktail)
        session.add_all([new_step, cocktail])
        session.flush()
        return cocktail

    @with_upper_scope_session
    def append_step_to_end_of_recipe(self, new_step: Step, validate: Optional[bool] = True, session: Session = None) -> Cocktail:
        """
        Append a new step to the end (tail) of a cocktail's recipe.
        If no steps, sets as head.
        """
        cocktail = new_step.cocktail
        session.refresh(cocktail)
        steps = cocktail.steps
        if not steps:
            new_step.is_recipe_first_step = True
            new_step.next_step = None
        else:
            last = steps[-1]
            last.next_step = new_step
            new_step.next_step = None
        if validate:
            self._validate_recipe_integrity(session, cocktail)
        session.add_all([new_step, cocktail])
        session.flush()
        return cocktail

    @with_upper_scope_session
    def insert_step_to_recipe_head(self, new_step: Step, validate: Optional[bool] = True, session: Session = None) -> Cocktail:
        """
        Insert a new step at the start (head) of a cocktail's recipe.
        - New step becomes head, points to previous head if any.
        """
        cocktail = new_step.cocktail
        session.refresh(cocktail)
        steps = cocktail.steps
        if steps:
            old_head = steps[0]
            old_head.is_recipe_first_step = False
            new_step.next_step = old_head
        else:
            new_step.next_step = None
        new_step.is_recipe_first_step = True
        if validate:
            self._validate_recipe_integrity(session, cocktail)
        session.add_all([new_step, cocktail])
        session.flush()
        return cocktail

    @with_upper_scope_session
    def associate_tag_with_cocktail(self, cocktail: Cocktail, tag: Tag, session: Session = None):
        """
        Associates a single tag with a cocktail.
        """
        cocktail_tag_association = CocktailTagAssociation(cocktail=cocktail, tag=tag)
        session.add(cocktail_tag_association)
        cocktail.cocktail_tag_associations.append(cocktail_tag_association)
        return cocktail

    @with_upper_scope_session
    def dissociate_tag_from_cocktail(self, cocktail: Cocktail, tag: Tag, session: Session = None):
        """
        Dissociates a single tag from a cocktail.
        """
        association = next((assoc for assoc in cocktail.cocktail_tag_associations if assoc.tag_id == tag.id), None)
        if association:
            cocktail.cocktail_tag_associations.remove(association)
            session.delete(association)
        return cocktail

    @with_upper_scope_session
    def associate_tags_with_cocktail(self, cocktail: Cocktail, tags: List[Tag], session: Session = None):
        """
        Associates multiple tags with a cocktail.
        """
        for tag in tags:
            if not any(assoc.tag_id == tag.id for assoc in cocktail.cocktail_tag_associations):
                cocktail_tag_association = CocktailTagAssociation(cocktail_id=cocktail.id, tag_id=tag.id)
                session.add(cocktail_tag_association)
                cocktail.cocktail_tag_associations.append(cocktail_tag_association)
        return cocktail

    @with_upper_scope_session
    def dissociate_tags_from_cocktail(self, cocktail: Cocktail, tags: List[Tag], session: Session = None):
        """
        Dissociates multiple tags from a cocktail.
        """
        for tag in tags:
            association = next((assoc for assoc in cocktail.cocktail_tag_associations if assoc.tag_id == tag.id), None)
            if association:
                cocktail.cocktail_tag_associations.remove(association)
                session.delete(association)
        return cocktail

    @with_upper_scope_session
    def dissociate_all_tags_from_cocktail(self, cocktail: Cocktail, session: Session = None):
        """
        Dissociates all tags from a cocktail.
        """
        for association in cocktail.cocktail_tag_associations:
            session.delete(association)
        cocktail.cocktail_tag_associations = []
        return cocktail
