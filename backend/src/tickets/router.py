from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.pagination import PaginatedResponse, PaginationParams
from src.tickets.dependencies import is_ticket_id_valid
from src.tickets.models import Ticket
from src.tickets.schemas import TicketResponseSchema, TicketCreateSchema, TicketBulkResponseSchema, \
    TicketCreateBulkSchema, TicketUpdateSchema, TicketPATCHSchema
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


@router.get(
    "/tickets/{ticket_id}",
    tags=["Tickets"],
    description="Get ticket by id",
    response_model=TicketResponseSchema,
    status_code=200)
async def get_ticket_by_id(
        ticket: Ticket = Depends(is_ticket_id_valid)):
    return ticket


@router.post(
    "/tickets",
    tags=["Tickets"],
    description="Create a new ticket",
    response_model=TicketResponseSchema,
    status_code=201)
async def create_ticket(
        ticket: TicketCreateSchema,
        db: AsyncSession = Depends(get_db)):
    return await ticket_service.create_ticket(db, ticket)


@router.post(
    "/tickets/bulk",
    tags=["Tickets"],
    description="Create a new ticket",
    response_model=TicketBulkResponseSchema,
    status_code=201)
async def create_tickets_bulk(
        bulk_ticket: TicketCreateBulkSchema,
        db: AsyncSession = Depends(get_db)
):
    return await ticket_service.create_ticket_bulk(db, bulk_ticket)


@router.put(
    "/tickets/{ticket_id}",
    tags=["Tickets"],
    description="Update the ticket",
    response_model=TicketResponseSchema,
    status_code=200)
async def update_ticket(
        update_data: TicketUpdateSchema,
        ticket: Ticket = Depends(is_ticket_id_valid),
        db: AsyncSession = Depends(get_db)
):
    return await ticket_service.update_ticket(db, ticket, update_data)


@router.patch(
    "/tickets/{ticket_id}",
    tags=["Tickets"],
    description="PATCH the ticket",
    response_model=TicketResponseSchema,
    status_code=200)
async def patch_ticket(
        update_data: TicketPATCHSchema,
        ticket: Ticket = Depends(is_ticket_id_valid),
        db: AsyncSession = Depends(get_db)
):
    return await ticket_service.patch_ticket(db, ticket, update_data)


@router.delete(
    "/tickets/{ticket_id}",
    tags=["Tickets"],
    description="Delete the ticket",
    status_code=204)
async def delete_ticket(
        ticket: Ticket = Depends(is_ticket_id_valid),
        db: AsyncSession = Depends(get_db)
):
    await ticket_service.delete_ticket(db, ticket)
