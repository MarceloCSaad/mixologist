from typing import Any, List, Optional
from sqlalchemy.orm import Session

from src.database.db_service import PGDatabaseService
from src.database.session_decorator import with_upper_scope_session
from src.models.tag import Tag


class TagService(PGDatabaseService):
    """
    Service to manage Tag-related database operations.
    """

    def __init__(self):
        super().__init__()

    def _get_filter_conditions(
        self, id: Optional[int], name: Optional[str]
    ) -> List[Any]:
        filter_conditions = []
        filter_conditions.append(Tag.id == id) if id else None
        filter_conditions.append(Tag.name == name) if name else None
        return filter_conditions

    @with_upper_scope_session
    def fetch_tags(
        self, id: Optional[int], name: Optional[str], session: Session = None
    ) -> List[Tag]:
        """
        Fetches tags from the database based on optional filters: id and name.
        If no filters are provided, all tags are returned.
        """
        if not id and not name:
            return session.query(Tag).all()
        tags = (
            session.query(Tag)
            .filter(*self._get_filter_conditions(id=id, name=name))
            .all()
        )
        return tags

    @with_upper_scope_session
    def fetch_tag_by_id(self, id: int, session: Session = None) -> Optional[Tag]:
        """
        Fetches a single tag by its ID.
        """
        return session.query(Tag).filter(Tag.id == id).first()

    @with_upper_scope_session
    def fetch_tag_by_name(self, name: str, session: Session = None) -> Optional[Tag]:
        """
        Fetches a single tag by its name.
        """
        return session.query(Tag).filter(Tag.name == name).first()

    @with_upper_scope_session
    def get_or_create_tag(self, name: str, session: Session = None) -> Tag:
        """
        Retrieves an existing tag by name or creates a new one if it doesn't exist.
        Handles race conditions and normalizes the name.
        """
        normalized_name = name.strip().lower()
        old_tag = self.fetch_tag_by_name(name=normalized_name, session=session)
        if old_tag:
            return old_tag
        new_tag = Tag(name=normalized_name)
        session.add(new_tag)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            # Try to fetch again in case of race condition
            old_tag = self.fetch_tag_by_name(name=normalized_name, session=session)
            if old_tag:
                return old_tag
            raise e
        session.refresh(new_tag)
        return new_tag
