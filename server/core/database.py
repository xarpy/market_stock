from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from server.core.settings import Settings, settings

_SESSION = None


class DBManager:
    """Client database manager"""

    def __init__(self, context: Settings = settings) -> None:
        self._context = context
        self._debug_mode = self._context.DB_DEBUG
        self.engine = self.create_engine()

    def create_engine(self) -> Engine:
        """Function responsible to create engine with all parameter with SQLAlchemy package.
        Returns:
            Engine: engine instance for postgres database.
        """
        engine = create_engine(
            self._context.SQLALCHEMY_DATABASE_URI.unicode_string(),
            pool_size=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=bool(self._debug_mode),
        )
        return engine

    def _create_db_session(self, engine: Engine) -> Session:
        """Function responsible to create and persist session sqlalchemy instance for database.
        Args:
            engine (Engine): Received a engine created with sqlalchemy

        Returns:
            Session: Return a session instance
        """
        global _SESSION
        if not _SESSION:
            _SESSION = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return _SESSION()

    def get_session(self) -> Session:
        """Function responsible to getting the session instance for specific database, based on parameter has taked.
        Args:
            type_instance (Optional[str]): Received a parameter to described the database need choose.
        Returns:
            Union[Any, Session]: Return session instance
        """
        session = self._create_db_session(self.engine)
        return session


db_manager = DBManager()


def get_db() -> Generator[Session, None, None]:
    db: Session = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()
