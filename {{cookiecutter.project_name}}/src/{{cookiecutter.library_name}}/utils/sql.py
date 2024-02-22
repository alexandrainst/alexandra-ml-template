""" Potsgresql connection to IoT database."""

import os
from pathlib import Path

# DEFINE THE DATABASE CREDENTIALS
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Determine the absolute path to the project repo
project_path = Path(__file__).parents[3]

A = load_dotenv(os.path.join(project_path, ".env"))
if not A:
    raise Exception(".env not loaded.")

A = load_dotenv()


DEFAULT_POSTGRES_USER = os.environ["POSTGRES_USER"]
DEFAULT_POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DEFAULT_POSTGRES_HOST = os.environ["POSTGRES_HOST"]
DEFAULT_POSTGRES_PORT = os.environ["POSTGRES_PORT"]
DEFAULT_POSTGRES_DB = os.environ["POSTGRES_DB"]


# -------------------------------------------------------------
class Base(DeclarativeBase):
    """SQLAlchemy Base class for ORM objects.

    In case we might want to load directly into other code.
    """
    pass

# ------------------------------------------------------------
def load_session(**modified_connection):
    """Load an SQL connection session.

    Return a session object that is aware
    of all necessary tables from the database
    """
    engine = get_connection(**modified_connection)
    SessionMaker = sessionmaker(bind=engine)
    # Create a session
    session = SessionMaker()

    Base.metadata.create_all(engine)

    return session


# get the connection engine
def get_connection(
    user=DEFAULT_POSTGRES_USER,
    password=DEFAULT_POSTGRES_PASSWORD,
    host=DEFAULT_POSTGRES_HOST,
    port=DEFAULT_POSTGRES_PORT,
    database=DEFAULT_POSTGRES_DB,
    ):
    """Return an sqlalchemy conenction engine."""
    return create_engine(
        url="postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
