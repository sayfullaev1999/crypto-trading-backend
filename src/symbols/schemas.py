from uuid import UUID

from pydantic import BaseModel, ConfigDict

from symbols.enums import SymbolType


class SymbolResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ticker: str
    display_name: str
    type: SymbolType
    is_active: bool
