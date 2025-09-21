from src.settings import PG_PASSWORD, PG_PORT, PG_USER, PG_HOST, PG_DB_NAME


POSTGRESQL__PSYCOPG2__DB_URI = (
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"
)
