from strawberry.types import Info
from strawberry import (
    type,
    mutation,
)

from config.exceptions import ProductDuplicated, ProductNotFound
from schemas.graphql.permission import (
    IsAuthenticated,
    IsAdmin,
)
from schemas.graphql.product import CreateProductInput, CreateProductResult, ProductError, UpdateProductInput, \
    UpdateProductResult, DeleteProductResult
from schemas.pydantic.product import ProductSchema
from services.product import add_product, updated_product, deleted_product


@type
class MutationProduct:
    @mutation(permission_classes=[IsAuthenticated, IsAdmin])
    def add_product(self, info: Info, product: CreateProductInput) -> CreateProductResult:
        try:
            user_data = ProductSchema(**product.__dict__)
            return add_product(info.context['db'], user_data)
        except ProductDuplicated as e:
            return ProductError(message=e.__str__())

    @mutation(permission_classes=[IsAuthenticated, IsAdmin])
    def update_product(self, info: Info, product: UpdateProductInput) -> UpdateProductResult:
        try:
            user_data = ProductSchema(**product.__dict__)
            return updated_product(info.context['db'], user_data)
        except ProductNotFound as e:
            return ProductError(message=e.__str__())

    @mutation(permission_classes=[IsAuthenticated, IsAdmin])
    def delete_product(self, info: Info, sku: str) -> DeleteProductResult:
        try:
            return deleted_product(info.context['db'], sku)
        except ProductNotFound as e:
            return ProductError(message=e.__str__())

