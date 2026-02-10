from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TicketBaseSchema(BaseModel):
    name: str
    price: float
    is_valid: bool


class TicketCreateSchema(TicketBaseSchema):
    user_id: Optional[int] = None


class TicketUpdateSchema(TicketBaseSchema):
    user_id: int = Field(ge=1)


class TicketCreateBulkSchema(TicketBaseSchema):
    amount: Optional[int] = Field(None, ge=10, le=10000)


class TicketPATCHSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(None, ge=1)
    is_valid: Optional[bool] = None
    user_id: Optional[int] = Field(None, ge=1)


class TicketResponseSchema(TicketBaseSchema):
    id: int
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TicketBulkResponseSchema(BaseModel):
    success: bool
    tickets_created: int


class TicketListResponseSchema(BaseModel):
    total: int
    tickets: list[TicketResponseSchema]

    model_config = ConfigDict(from_attributes=True)
