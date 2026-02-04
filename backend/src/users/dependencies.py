from fastapi import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from service import user_service
from src.users.models import User


async def is_user_id_valid(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    user = await user_service.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
