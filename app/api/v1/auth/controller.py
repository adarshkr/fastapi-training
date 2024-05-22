import typing as t
from datetime import timedelta
from pydantic import BaseModel
from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from app.config import config
from app.crud.user import user as CRUDUser
from app.api.dependencies.security import get_password_hash, get_token_payload, verify_password
from app.models.user import User
from app.api.dependencies import security


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class AuthApi:
    def authenticate(
        self, session: Session, *, username: str, password: str
    ) -> t.Optional[dict]:

        user = CRUDUser.get_user(
            session, username=username
        )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        data = {"sub": f"{user.id}"}
        return self._get_user_token(data, refresh_token=None)

    def _authenticate_master_admin(
        self, session: Session, *, username: str, password: str
    ) -> t.Optional[User]:
        user = CRUDUser.get_user(session, username=username)

        if not user or user.disabled:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user


    def _get_user_token(self, data: dict, refresh_token=None):

        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = security.create_access_token(
            data=data,
            expires_delta=access_token_expires,
        )

        if not refresh_token:
            refresh_token = security.create_refresh_token(data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=access_token_expires.seconds,  # in seconds
        )

    def get_refresh_token(self, session: Session, *, token: str):
        payload = get_token_payload(token=token)
        user_id = payload.get("sub", None)

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = CRUDUser.get(session, id=user_id)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        data = {"sub": user.id}
        return self._get_user_token(data=data, refresh_token=token)

    @staticmethod
    def get_user_details(
        session: Session,
        *,
        request: Request,
    ) -> dict:

        if isinstance(request.user, User):
            return {**request.user.to_dict()}

        user = request.user.to_dict()
        
        return user

