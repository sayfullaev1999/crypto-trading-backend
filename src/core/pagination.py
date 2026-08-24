from dataclasses import dataclass
from math import ceil
from typing import TypeVar, Generic

from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    pagination: PaginationMeta


def get_pagination(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> PaginationParams:
    return PaginationParams(
        page=page,
        page_size=page_size
    )


@dataclass(slots=True)
class PaginationResult(Generic[T]):
    items: list[T]
    total: int
    pages: int


async def paginate(
    session: AsyncSession,
    query,
    pagination: PaginationParams,
) -> PaginationResult[T]:
    count_query = select(
        func.count()
    ).select_from(
        query.order_by(None).subquery()
    )

    total = await session.scalar(count_query) or 0
    result = await session.execute(
        query
        .offset(pagination.offset)
        .limit(pagination.page_size)
    )

    items = list(result.scalars().all())
    pages = ceil(total / pagination.page_size) if total else 0
    return PaginationResult(
        items=items,
        total=total,
        pages=pages
    )
