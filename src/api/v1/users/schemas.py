from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCredentials(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: bytes
    email: EmailStr | None = None
    is_active: bool = True

    model_config = ConfigDict(strict=True)
