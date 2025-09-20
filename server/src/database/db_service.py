from sqlalchemy import create_engine, Engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker, Session

from src.database.constants import POSTGRESQL__PSYCOPG2__DB_URI as pg_uri


class DBModel():
    def __init__(self) -> None:
        self.engine = self._get_pg_engine_from_settings()
        super().__init__()

    def _get_pg_engine_from_settings(self) -> Engine:
        if not database_exists(pg_uri):
            print("Database does not exist. Creating...")
            create_database(pg_uri)

        return create_engine(pg_uri, echo=False)

    def get_session(self) -> Session:
        """
        Create a SQLAlchemy session instance.
        """
        return sessionmaker(bind=self.engine)()


class PGDatabaseService(DBModel):
    """
    Service to manage PostgreSQL database connections and operations.
    """

    def __init__(self) -> None:
        super().__init__()

    def create_tables(self) -> None:
        from src.models.base_model import BaseModel
        """
        Create all tables in the database.
        """
        print("Creating all tables...")
        BaseModel.metadata.create_all(self.engine)

    def get_db_uri(self) -> str:
        """
        Get the PostgreSQL database URI.
        """
        return self.engine.url