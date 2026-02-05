from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.pagination import PaginatedResponse, PaginationParams
from src.tickets.schemas import TicketResponseSchema
from src.tickets.service import ticket_service

router = APIRouter()


@router.get(
    "/tickets",
    tags=["Tickets"],
    description="Get all tickets",
    response_model=PaginatedResponse[TicketResponseSchema],
    status_code=200)
async def get_paginated_tickets(
        pagination: PaginationParams = Depends(),
        db: AsyncSession = Depends(get_db)):
    tickets, total = await ticket_service.get_tickets(db, pagination)

    return PaginatedResponse.create(tickets, total, pagination)