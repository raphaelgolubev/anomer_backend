from uuid import UUID

from pydantic import EmailStr, BaseModel


class UserCreateIn(BaseModel):
    email: EmailStr
    password: str


class UserCreateOut(BaseModel):
    id: UUID


class UserRead(BaseModel):
    id: UUID
    email: str


class UserDeleteOut(BaseModel):
    is_deleted: bool


class EmailVerificationIn(BaseModel):
    id: UUID
    email: EmailStr


class EmailVerificationOut(BaseModel):
    message: str


class VerifyCodeIn(BaseModel):
    email: EmailStr
    code: str


class VerifyCodeOut(BaseModel):
    verified: bool
    message: str
