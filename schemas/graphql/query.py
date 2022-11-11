from strawberry import type, field
from schemas.graphql.product import Product


@type
class Query:
    @field
    def product(self) -> Product:
        return Product(sku="test", name="test", price=1.2, brand="lacteo")
