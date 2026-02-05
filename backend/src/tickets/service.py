from typing import Tuple, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.pagination import PaginationParams
from src.tickets.models import Ticket


class TicketService:
    async def get_tickets(self, db: AsyncSession, pagination: PaginationParams) -> Tuple[Sequence[Ticket], int]:
        count_result = await db.execute(func.count(Ticket.id))
        total = count_result.scalar()

        tickets_result = await db.execute(
            select(Ticket)
            .order_by(Ticket.created_at)
            .offset(pagination.skip)
            .limit(pagination.limit)
        )
        tickets = tickets_result.scalars().all()

        return list(tickets), total


ticket_service = TicketService()