from typing import Optional

from pydantic import BaseModel


from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    email: Optional[str]
    name: str
    idCompany: Optional[int]
    isOwner: bool


class UserCreate(schemas.BaseUserCreate):
    email: Optional[str]
    idCompany: Optional[int]
    password: str
    login: str
    name: str
    isOwner: bool


class UserUpdate(schemas.BaseUserUpdate):
    id: int
    name: Optional[str]
    login: Optional[str]
    idCompany: Optional[int]
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
