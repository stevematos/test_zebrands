from strawberry import input, type, union


@input
class ProductInput:
    sku: str
    name: str
    price: float
    brand: str


class CreateProductInput(ProductInput):
    pass


@input
class UpdateProductInput(ProductInput):
    name: str | None = None
    price: float | None = None
    brand: str | None = None


@type
class ProductResponse:
    sku: str
    name: str
    price: float
    brand: str


@type
class GetProductResponse(ProductResponse):
    pass


@type
class CreateProductResponse(ProductResponse):
    pass


@type
class UpdateProductResponse(ProductResponse):
    pass


@type
class DeleteProductResponse(ProductResponse):
    message: str


@type
class ProductError:
    message: str


GetProductResult = union(
    "GetProductResult", (GetProductResponse, ProductError)
)
CreateProductResult = union(
    "CreateProductResult", (CreateProductResponse, ProductError)
)
UpdateProductResult = union(
    "UpdateProductResult", (UpdateProductResponse, ProductError)
)
DeleteProductResult = union(
    "DeleteProductResult", (DeleteProductResponse, ProductError)
)
