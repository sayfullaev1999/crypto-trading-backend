from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi.routing import APIRouter
from fastapi import status, Depends

from core.pagination import PaginatedResponse, PaginationParams, get_pagination, PaginationMeta
from symbols.schemas import SymbolResponse
from symbols.service import SymbolService
from users.models import User

router = APIRouter(
    prefix="/api/symbols",
    tags=["Symbols"],
    route_class=DishkaRoute
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[SymbolResponse],
)
async def get_symbols(
    pagination: Annotated[
        PaginationParams,
        Depends(get_pagination)
    ],
    current_user: FromDishka[User],
    symbol_service: FromDishka[SymbolService],
) -> PaginatedResponse[SymbolResponse]:
    result = await symbol_service.get_symbols(pagination)
    return PaginatedResponse(
        items=result.items,
        pagination=PaginationMeta(
            page=pagination.page,
            page_size=pagination.page_size,
            total=result.total,
            pages=result.pages
        ),
    )
