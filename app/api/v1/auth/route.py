from typing import Any

from fastapi import APIRouter, Depends, Request, Header, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.auth.controller import AuthApi
from app.core.base_response import BaseResponse
from app.db.session import acquire_db_session
from app.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.API_V1_STR}/auth/token")

auth_router = r = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

user_router = APIRouter(
    prefix="/me",
    tags=["User"],
)


@r.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(acquire_db_session),
) -> Any:
    auth_api = AuthApi()
    token = auth_api.authenticate(
        session,
        username=form_data.username,
        password=form_data.password,
    )

    return BaseResponse.from_result(result={**token.model_dump()}).dict()

@r.post("/generate-token")
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(acquire_db_session),
) -> Any:
    auth_api = AuthApi()
    token = auth_api.authenticate(
        session,
        username=form_data.username,
        password=form_data.password,
    )
    return {"access_token": token.access_token, "token_type": "bearer"}

@r.post("/refresh")
async def refresh_access_token(
    token: str = Header(), session: Session = Depends(acquire_db_session)
):
    auth_api = AuthApi()
    token = auth_api.get_refresh_token(
        session,
        token=token,
    )
    return BaseResponse.from_result(result={**token.model_dump()}).dict()


@user_router.get("")
async def get_user_details(
    request: Request,
    session: Session = Depends(acquire_db_session),
) -> dict:
    return BaseResponse.from_result(result={**request.user}).dict()
