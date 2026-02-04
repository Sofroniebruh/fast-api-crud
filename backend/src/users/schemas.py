from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, EmailStr, ConfigDict, Field

# Useful to prevent circular dep issue. TYPE_CHECKING is always false at runtime, so no error.
# Meanwhile, IDE pretends it's true.
if TYPE_CHECKING:
    from src.tickets.schemas import TicketResponseSchema


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserPatchSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr]


class UserCreateSchema(UserBaseSchema):
    password: str


class UserResponseSchema(UserBaseSchema):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    # Forward reference (usage of ""), means Python doesn't evaluate it immediately, just stores it as a string.
    # Pydantic resolves it later using model_rebuild().
    tickets: List["TicketResponseSchema"]

    # Basically allows to read from DB ORM model,
    # because naturally pydantic schemas are expecting dicts, not ORM objects
    model_config = ConfigDict(from_attributes=True)


class UserListResponseSchema(BaseModel):
    users: list[UserResponseSchema]
    total: int

    model_config = ConfigDict(from_attributes=True)
