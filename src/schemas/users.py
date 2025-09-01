from pydantic import EmailStr, BaseModel


# GET /users/
class UserRead(BaseModel):
    id: int
    email: str


# /create/
# ---
class UserCreateIn(BaseModel):
    email: EmailStr
    password: str


class UserCreateOut(BaseModel):
    """Информацию о созданном пользователе или об ошибке"""

    id: int | None = None
    created: bool
    message: str


# /delete/{id}
# ---
class UserDeleteOut(BaseModel):
    deleted: bool
    message: str


# /send-verification/
# ---
class EmailVerificationIn(BaseModel):
    id: int


class EmailVerificationOut(BaseModel):
    sent: bool = True
    message: str
    code_expires_in_seconds: int = None


# /verify-code/
# ---
class VerifyCodeIn(BaseModel):
    email: EmailStr
    code: str


class VerifyCodeOut(BaseModel):
    verified: bool
    message: str
