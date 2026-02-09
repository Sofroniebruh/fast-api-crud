import logging
from typing import Tuple, Sequence, Optional

from fastapi import HTTPException
from sqlalchemy import func, select, insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import AsyncSessionLocal
from src.pagination import PaginationParams
from src.users.models import User
from src.utils import chunked
from src.tickets.models import Ticket
from src.tickets.schemas import TicketCreateSchema, TicketCreateBulkSchema, TicketUpdateSchema, TicketPATCHSchema

logger = logging.getLogger(__name__)


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

    async def create_ticket(self, db: AsyncSession, ticket: TicketCreateSchema) -> Ticket:
        db_ticket = Ticket(
            user_id=ticket.user_id if ticket.user_id else None,
            price=ticket.price,
            name=ticket.name,
            is_valid=ticket.is_valid,
        )

        db.add(db_ticket)
        await db.commit()
        await db.refresh(db_ticket)

        return db_ticket

    async def create_ticket_bulk(self, db: AsyncSession, ticket: TicketCreateBulkSchema) -> dict:
        if ticket.amount > 5000:
            try:
                await self.create_tickets_background(ticket.name, ticket.amount, ticket.is_valid, ticket.price)

                return {
                    "success": True,
                    "tickets_created": ticket.amount,
                }
            except SQLAlchemyError as e:
                await db.rollback()
                logger.error(f"Bulk ticket creation failed: {str(e)}")

                raise HTTPException(500, "Failed to create tickets")
        else:
            try:
                ticket_records = [
                    {
                        "price": ticket.price,
                        "name": ticket.name,
                        "is_valid": ticket.is_valid,
                    }
                    for _ in range(ticket.amount)
                ]

                CHUNK_SIZE = 500

                for chunk in chunked(ticket_records, CHUNK_SIZE):
                    stmt = insert(Ticket).values(chunk)

                    await db.execute(stmt)

                await db.commit()

                return {
                    "success": True,
                    "tickets_created": ticket.amount,
                }
            except SQLAlchemyError as e:
                await db.rollback()
                logger.error(f"Bulk ticket creation failed: {str(e)}")

                raise HTTPException(500, "Failed to create tickets")

    async def update_ticket(self, db: AsyncSession, ticket: Ticket, update_data: TicketUpdateSchema) -> Ticket:
        if update_data.user_id and not await self._validate_user_id(db, update_data.user_id):
            raise HTTPException(400, "Invalid user_id")

        update_dict = update_data.model_dump(exclude_unset=False)
        return await self._update_and_save(db, ticket, update_dict)

    async def patch_ticket(self, db: AsyncSession, ticket: Ticket, update_data: TicketPATCHSchema) -> Ticket:
        if update_data.user_id and not await self._validate_user_id(db, update_data.user_id):
            raise HTTPException(400, "Invalid user_id")

        update_dict = update_data.model_dump(exclude_unset=True)
        return await self._update_and_save(db, ticket, update_dict)

    async def create_tickets_background(
            self,
            name: str,
            amount: int,
            is_valid: bool,
            price: float
    ):
        async with AsyncSessionLocal() as db:
            ticket_records = [
                {
                    "price": price,
                    "name": name,
                    "is_valid": is_valid,
                }
                for _ in range(amount)
            ]

            for chunk in chunked(ticket_records, 1000):
                stmt = insert(Ticket).values(chunk)
                await db.execute(stmt)

            await db.commit()

    async def _validate_user_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        user = await db.execute(
            select(User)
            .where(User.id == user_id)
        )

        return user.scalar_one_or_none()

    async def _update_and_save(self, db: AsyncSession, ticket: Ticket, update_data: dict) -> Ticket:
        for field, value in update_data.items():
            setattr(ticket, field, value)

        try:
            db.add(ticket)
            await db.commit()
            await db.refresh(ticket)

            return ticket
        except IntegrityError as e:
            await db.rollback()
            raise ValueError(f"Database integrity error: {e}")


ticket_service = TicketService()
