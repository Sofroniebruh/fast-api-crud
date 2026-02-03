from typing import Optional

from pydantic import BaseModel, ConfigDict


class TicketBaseSchema(BaseModel):
    name: str
    price: float
    is_valid: bool
    amount: int


class TicketUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    is_valid: Optional[bool] = None
    amount: Optional[int] = None
    user_id: Optional[int] = None


class TicketResponseSchema(TicketBaseSchema):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class TicketListResponseSchema(BaseModel):
    total: int
    tickets: list[TicketResponseSchema]

    model_config = ConfigDict(from_attributes=True)
