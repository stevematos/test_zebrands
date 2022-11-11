from strawberry import type


@type
class Product:
    sku: str
    name: str
    price: float
    brand: str
