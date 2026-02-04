from fastapi import HTTPException, Query
from fastapi.param_functions import Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from service import user_service
from src.users.models import User


class PaginationParams(BaseModel):
    page: int = Field(ge=1, description="The page number")
    page_size: int = Field(ge=5, le=100, description="The number of items to return")

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.limit

    @property
    def limit(self):
        return self.page_size

    def __init__(
            self,
            page: int = Query(1, ge=1, description="The page number"),
            page_size: int = Query(5, ge=5, le=100, description="The number of items to return")):
        super().__init__(page=page, page_size=page_size)


async def is_user_id_valid(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    user = await user_service.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
