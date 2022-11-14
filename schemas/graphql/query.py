from strawberry import type, field
from schemas.graphql.product import CreateProductResponse


@type
class Query:
    @field
    def product(self) -> CreateProductResponse:
        return CreateProductResponse(sku="test", name="test", price=1.2)
