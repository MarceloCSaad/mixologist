from typing import Any, List, Optional
from sqlalchemy.orm import Session

from src.database.db_service import PGDatabaseService
from src.database.session_decorator import with_upper_scope_session
from src.models.ingredient import Ingredient


class IngredientService(PGDatabaseService):
    """
    Service to manage Ingredient-related database operations.
    """

    def __init__(self):
        super().__init__()

    def _get_filter_conditions(
        self, id: Optional[int], name: Optional[str]
    ) -> List[Any]:
        filter_conditions = []
        filter_conditions.append(Ingredient.id == id) if id else None
        filter_conditions.append(Ingredient.name == name) if name else None
        return filter_conditions

    @with_upper_scope_session
    def fetch_ingredients(
        self, id: Optional[int], name: Optional[str], session: Session = None
    ) -> List[Ingredient]:
        """
        Fetches ingredients from the database based on optional filters: id and name.
        If no filters are provided, all ingredients are returned.
        """
        if not id and not name:
            return session.query(Ingredient).all()
        return (
            session.query(Ingredient)
            .filter(*self._get_filter_conditions(id=id, name=name))
            .all()
        )

    @with_upper_scope_session
    def fetch_ingredient_by_id(
        self, id: int, session: Session = None
    ) -> Optional[Ingredient]:
        """
        Fetches a single ingredient by its ID.
        """
        return session.query(Ingredient).filter(Ingredient.id == id).first()

    @with_upper_scope_session
    def fetch_ingredient_by_name(
        self, name: str, session: Session = None
    ) -> Optional[Ingredient]:
        """
        Fetches a single ingredient by its name.
        """
        return session.query(Ingredient).filter(Ingredient.name == name).first()

    @with_upper_scope_session
    def get_or_create_ingredient(
        self, name: str, session: Session = None
    ) -> Ingredient:
        """
        Retrieves an ingredient by name or creates one if none exist.
        Handles race conditions and normalizes the name.
        """
        normalized_name = name.strip().lower()
        old_ingredient = self.fetch_ingredient_by_name(
            name=normalized_name, session=session
        )
        if old_ingredient:
            return old_ingredient
        new_ingredient = Ingredient(name=normalized_name)
        session.add(new_ingredient)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            # Try to fetch again in case of race condition
            old_ingredient = self.fetch_ingredient_by_name(
                name=normalized_name, session=session
            )
            if old_ingredient:
                return old_ingredient
            raise e
        session.refresh(new_ingredient)
        return new_ingredient
