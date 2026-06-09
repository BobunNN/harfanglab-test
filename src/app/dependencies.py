from functools import lru_cache
from typing import Generator

from sqlmodel import Session, create_engine

from src.app.config import get_settings


@lru_cache
def get_engine():
    return create_engine(get_settings().database_url, echo=False)


def get_db() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session
