import hashlib
from collections.abc import Sequence
from typing import Optional, Tuple

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.pagination import PaginationParams
from src.users.models import User
from src.users.schemas import UserCreateSchema, UserBaseSchema, UserPatchSchema


class UserService:
    async def create_user(self, db: AsyncSession, user: UserCreateSchema) -> User:
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        db_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_users(self, db: AsyncSession, pagination: PaginationParams) -> Tuple[Sequence[User], int]:
        count_result = await db.execute(select(func.count(User.id)))
        total = count_result.scalar()

        users_result = await db.execute(
            select(User)
            .order_by(User.created_at)
            .offset(pagination.skip)
            .limit(pagination.limit)
        )

        users = users_result.scalars().all()

        return list(users), total

    async def patch_user(self, db: AsyncSession, user: User, update_data: UserPatchSchema) -> User:
        user_data = update_data.model_dump(exclude_unset=True)

        if not user_data:
            return user

        return await self._update_and_save(db, user, user_data)

    async def update_user(self, db: AsyncSession, user: User, update_data: UserBaseSchema) -> User:
        user_data = update_data.model_dump(exclude_unset=False)

        return await self._update_and_save(db, user, user_data)

    async def delete_user(self, db: AsyncSession, user: User) -> None:
        await db.delete(user)
        await db.commit()

    async def _update_and_save(self, db: AsyncSession, user: User, update_data: dict) -> User:
        for field, value in update_data.items():
            setattr(user, field, value)

        try:
            db.add(user)
            await db.commit()
            await db.refresh(user)

            return user
        except IntegrityError as e:
            await db.rollback()
            raise ValueError(f"Database integrity error: {e}")


user_service = UserService()
