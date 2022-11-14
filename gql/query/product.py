from strawberry.types import Info

from strawberry import type, field

from config.exceptions import ProductNotFound
from schemas.graphql.permission import IsAuthenticated
from schemas.graphql.product import GetProductResult, ProductError
from services.product import get_product


@type
class QueryProduct:
    @field(permission_classes=[IsAuthenticated])
    def get_product(self, info: Info,  sku: str) -> GetProductResult:
        try:
            return get_product(info.context['db'], sku, info.context['email'])
        except ProductNotFound as e:
            return ProductError(message=e.__str__())
