from config.exceptions import ProductNotFound
from schemas.graphql.permission import IsAuthenticated
from schemas.graphql.product import GetProductResult, ProductError
from services.product import get_product
from strawberry import field, type
from strawberry.types import Info


@type
class QueryProduct:
    @field(permission_classes=[IsAuthenticated])
    def get_product(self, info: Info, sku: str) -> GetProductResult:
        try:
            return get_product(
                info.context["db"], sku, info.context["user_id"]
            )
        except ProductNotFound as e:
            return ProductError(message=e.__str__())
