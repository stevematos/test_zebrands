from strawberry import type, field
from schemas.graphql.product import ProductResponse


@type
class Query:
    @field
    def product(self) -> ProductResponse:
        return ProductResponse(sku="test", name="test", price=1.2)
