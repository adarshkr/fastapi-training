from datetime import datetime

from pydantic import BaseModel


class UsersBase(BaseModel):
    username: str

class UsersBaseCreate(UsersBase):
    password: str


class UsersCreateResponse(BaseModel):
    id: int


class UsersResponse(UsersBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UsersEdit(BaseModel):
    password: str
