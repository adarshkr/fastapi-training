import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.user.controller import UserApi
from app.core.base_response import BaseResponse
from app.db.session import acquire_db_session
from app.schemas.user import UsersBaseCreate, UsersCreateResponse, UsersEdit, UsersResponse

logger = logging.getLogger(__name__)


user_router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@user_router.get("", response_model=dict)
def get_users(
    session: Session = Depends(acquire_db_session),
) -> dict:
    users = UserApi.get_users(session)
    return BaseResponse.from_result(result=users).dict()
   

@user_router.get("/{username}", response_model=dict)
def get_user(
    username: str,
    session: Session = Depends(acquire_db_session),
) -> dict:
    user = UserApi.get_user_by_name(session, username=username)
    return BaseResponse.from_result(result=UsersResponse(**user)).dict()


@user_router.post("", response_model=dict)
def create_user(
    user: UsersBaseCreate,
    session: Session = Depends(acquire_db_session),
) -> dict:
    user_id: int = UserApi.create_user(session, user=user)
    return BaseResponse.from_result(result=UsersCreateResponse(id=user_id)).dict()
    

@user_router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(
    id: int,
    user: UsersEdit,
    session: Session = Depends(acquire_db_session),
) -> None:
    UserApi.update_user(session, id=id, user=user)
    

@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    session: Session = Depends(acquire_db_session),
) -> None:
    UserApi.delete_user(session, id=id)
    