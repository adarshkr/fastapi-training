from typing import Any, Dict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.security import get_password_hash
from app.crud.user import user as CRUDUser
from app.schemas.user import UsersBaseCreate, UsersEdit, UsersResponse

class ExceptionCustom(HTTPException):
    pass


class UserApi:
    @staticmethod
    def create_user(session: Session, *, user: UsersBaseCreate) -> int:
        return CRUDUser.create(session, obj_in=UsersBaseCreate(username=user.username, password=get_password_hash(user.password))).id

    @staticmethod
    def get_users(session: Session) -> list[UsersResponse]:
        users = CRUDUser.get_multi(session)
        return [UsersResponse(**user.to_dict()) for user in users]

    @staticmethod
    def get_user_by_name(session: Session, *, username: str) -> Dict[Any, Any]:
        user = CRUDUser.get_user(session, username=username)

        if not user:
            raise ExceptionCustom(status_code=400, detail="User not found")

        return user.to_dict()

    @staticmethod
    def get_user_by_id(session: Session, *, id: int) -> Dict[Any, Any] | None:
        user = CRUDUser.get(session, id=id)

        if not user:
            raise ExceptionCustom(status_code=400, detail="User not found")

        return user.to_dict()

    @staticmethod
    def update_user(session: Session, *, id: int, user: UsersEdit) -> None:
        db_obj = CRUDUser.get(session, id=id)
        if not db_obj:
            raise ExceptionCustom(status_code=400, detail="User not found")

        CRUDUser.update(session, db_obj=db_obj, obj_in=UsersEdit(password=get_password_hash(user.password)))

    @staticmethod
    def delete_user(session: Session, *, id: int) -> None:
        db_obj = CRUDUser.get(session, id=id)
        if not db_obj:
            raise ExceptionCustom(status_code=400, detail="User not found")
        CRUDUser.remove(session, id=id)
