from strawberry.types import Info
from strawberry import (
    type,
    mutation,
)

from schemas.graphql.permission import (
    IsAuthenticated,
    IsAdmin,
)
from schemas.graphql.product import ProductInput, ProductResponse


@type
class MutationProduct:
    @mutation(permission_classes=[IsAuthenticated, IsAdmin])
    def add_product(self, info: Info, product: ProductInput) -> ProductResponse:
        return ProductResponse(name="test")
