from functools import wraps

from src.models.base_model import BaseModel


def with_upper_scope_session(func):
    """
    Decorator for service methods to provide SQLAlchemy session management.
    If a 'session' keyword argument is provided, it is used as-is.
    If not, the decorator creates a new session using self.get_session(),
    injects it into the method call, commits after execution, and closes automatically.
    This allows methods to be used both with upper-scope sessions (for transaction control)
    or standalone with automatic session handling.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        session = kwargs.get('session')
        if session is not None:
            session.flush()  # Ensure all pending changes are flushed before manipulation
            result = func(self, *args, **kwargs)
            session.flush()
            return result
        with self.get_session() as session:
            kwargs['session'] = session
            session.flush()  # Ensure all pending changes are flushed before manipulation
            result = func(self, *args, **kwargs)
            session.commit()
            session.flush()
            if isinstance(result, BaseModel):
                session.refresh(result)
            elif isinstance(result, list) and all(isinstance(item, BaseModel) for item in result):
                for item in result:
                    session.refresh(item)
            return result
    return wrapper
