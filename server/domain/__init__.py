from abc import ABC

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()
metadata = Base.metadata


class BaseRepository(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session
