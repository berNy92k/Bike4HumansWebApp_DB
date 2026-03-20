from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class BikeReadDto(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    brand: str | None = None
    category: str | None = None
    price: Decimal
    stock_quantity: int
    image_url: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime