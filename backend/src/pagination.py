import math
from typing import Generic, TypeVar, List

from fastapi import Query
from pydantic import BaseModel, Field


T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(ge=1, description="The page number")
    page_size: int = Field(ge=5, le=100, description="The number of items to return")

    # With @property can be called without ()
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self):
        return self.page_size

    def __init__(
            self,
            page: int = Query(1, ge=1, description="The page number"),
            page_size: int = Query(5, ge=5, le=100, description="The number of items to return")):
        super().__init__(page=page, page_size=page_size)


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    meta: PaginationMeta

    # Without this annotation we need the instance of the class first,
    # but with @classmethod - can call direct on class, like static, but with power of accessing class itself or creating instances
    @classmethod
    def create(
            cls,
            items: List[T],
            total: int,
            pagination: PaginationParams,
    ):
        total_pages = math.ceil(total / pagination.page_size) if total > 0 else 0

        meta = PaginationMeta(
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total,
            total_pages=total_pages,
            has_next=pagination.page < total_pages,
            has_previous=pagination.page > 1
        )

        return cls(items=items, meta=meta)