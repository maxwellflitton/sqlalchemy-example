from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from config import GlobalParams


class DbEngine:
    """
    This is an class for managing the connection and game_sessions to the database.

    Attributes:
        engine (sqlalchemy.create_engine.return_value): connection to DB
        session (sqlalchemy.orm.sessionmaker.return_value): manages game_sessions with database
    """
    BASE = declarative_base()

    def __init__(self):
        """
        The constructor for the DbEngine class.
        """
        params = GlobalParams()
        self.engine = create_engine(params.get("DB_URL"), echo=True, pool_recycle=3600)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.url = params.get("DB_URL")
