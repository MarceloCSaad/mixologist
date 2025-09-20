from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env.development')

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB_NAME = os.getenv("PG_DB_NAME")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
