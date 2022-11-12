from strawberry import type, input


@input
class ProductInput:
    sku: str
    name: str
    price: float
    brand: str


@type
class ProductResponse:
    sku: str
    name: str
    price: float
