from typing import Annotated
from uuid import UUID

from pydantic import Field, EmailStr, BaseModel, ConfigDict


class UserCredentials(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: bytes
    email: EmailStr | None = None
    is_active: bool = True

    model_config = ConfigDict(strict=True)


class UserCreateIn(BaseModel):
    email: EmailStr
    password: str


class UserCreateOut(BaseModel):
    id: UUID


class UserRead(BaseModel):
    id: UUID
    email: str