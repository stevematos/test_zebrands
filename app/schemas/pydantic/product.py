from pydantic import BaseModel


class ProductSchema(BaseModel):
    sku: str
    name: str | None = None
    price: float | None = None
    brand: str | None = None


class ProductChange(BaseModel):
    email: str
    sku: str
    user_id: int
    product_id: int
    product_change: dict
