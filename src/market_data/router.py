from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from market_data.schemas import MarketDataSubscription
from market_data.service import MarketDataService


router = APIRouter(
    prefix="/market-data",
    tags=["Market Data"],
    route_class=DishkaRoute,
)


@router.websocket("/ws")
async def market_data_websocket(
    websocket: WebSocket,
    market_data_service: FromDishka[MarketDataService],
):
    await market_data_service.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            subscription = MarketDataSubscription.model_validate(data)

            if subscription.action == "subscribe":
                await market_data_service.subscribe(
                    websocket,
                    subscription.symbols,
                )

    except WebSocketDisconnect:
        market_data_service.disconnect(websocket)
