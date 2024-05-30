import logging

from app.db.init_db import init_db
from app.db.session import acquire_db_session

logger = logging.getLogger(__name__)


def init() -> None:
    session = acquire_db_session()
    init_db(session)


if __name__ == "__main__":
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")
