from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import config

db_engine = create_engine(config.RDS_URI, pool_pre_ping=True, echo=True)
db_session_maker = sessionmaker(bind=db_engine)


def acquire_db_session() -> Generator:
    session = db_session_maker()
    session.begin()
    try:
        yield session
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()
