from typing import Optional
from pydantic import BaseModel


class ProductSchema(BaseModel):
    sku: str
    name:  Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
