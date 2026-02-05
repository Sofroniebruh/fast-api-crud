from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.tickets.models import Ticket
from src.tickets.service import ticket_service


async def is_ticket_id_valid(ticket_id: int, db: AsyncSession = Depends(get_db)) -> Ticket:
    ticket = await ticket_service.get_ticket_by_id(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket
