from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UsersBaseCreate, UsersEdit


class CRUDUser(CRUDBase[User, UsersBaseCreate, UsersEdit]):
    def get_user(
        self, session: Session, *, username: str, password: str | None = None
    ) -> User | None:
        query = session.query(User).filter(User.username == username)

        if password:
            query = query.filter(User.password == password)

        user = query.first()

        if not user:
            return None

        return user


user = CRUDUser(User)
