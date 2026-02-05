from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, EmailStr, ConfigDict, Field

# Useful to prevent circular dep issue. TYPE_CHECKING is always false at runtime, so no error.
# Meanwhile, IDE pretends it's true.
if TYPE_CHECKING:
    from src.schemas import TicketResponseSchema


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserPatchSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=3)
    # If you want the field optional - add None,
    # without it pydantic treats them as required even with Optional[]
    email: Optional[EmailStr] = None


class UserCreateSchema(UserBaseSchema):
    password: str


class UserResponseSchema(UserBaseSchema):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    # Forward reference using quotes prevents circular import issues
    # The string "TicketResponseSchema" is resolved when model_rebuild() is called
    # Made Optional to handle cases where tickets aren't loaded (lazy="noload")
    tickets: Optional[List["TicketResponseSchema"]] = None

    # Basically allows to read from DB ORM model,
    # because naturally pydantic schemas are expecting dicts, not ORM objects
    model_config = ConfigDict(from_attributes=True)


class UserListResponseSchema(BaseModel):
    users: list[UserResponseSchema]
    total: int

    model_config = ConfigDict(from_attributes=True)

# Model rebuild moved to avoid import issues - will be handled at startup
