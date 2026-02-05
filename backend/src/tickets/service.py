from typing import Tuple, Sequence, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.pagination import PaginationParams
from src.tickets.models import Ticket


class TicketService:
    async def get_ticket_by_id(self, db: AsyncSession, ticket_id: int) -> Optional[Ticket]:
        ticket_result = await db.execute(
            select(Ticket)
            .where(Ticket.id == ticket_id)
        )

        return ticket_result.scalar_one_or_none()


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