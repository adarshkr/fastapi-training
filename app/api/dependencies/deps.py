from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.authentication import AuthCredentials, UnauthenticatedUser
import logging
from fastapi import HTTPException, status

from app.config import config
from app.api.v1.user.controller import UserApi
from app.db.session import acquire_db_session

logger = logging.getLogger(__name__)

class JWTAuth:

    async def authenticate(self, http_conn):
        logger.info("Authenticating user")
    
        guest = AuthCredentials(["unauthenticated"]), UnauthenticatedUser()

        session: Session = None

        if "authorization" not in http_conn.headers:
            logger.error("authorization not found")
            return guest

        token = http_conn.headers.get("authorization").split()[-1]  # Bearer token_hash

        if not token:
            logger.error("Token not found")
            return guest

        try:
            payload = jwt.decode(
                token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
            )
            user_id: str = payload.get("sub")

            if user_id is None:
                logger.error("Sub not found")
                return guest

        except JWTError as e:
            logger.error(f"Token error: {str(e)}")
            return guest

        if not session:
            session = next(acquire_db_session())

        user = UserApi.get_user_by_id(session, id=int(user_id))

        if user is None:
            logger.error("User not found")
            return guest

        logger.info("Authenticated user")

        return (
            AuthCredentials("authenticated"),
            dict(
                **user,
            )
        )
