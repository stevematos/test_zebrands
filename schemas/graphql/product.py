from typing import Optional

from strawberry import type, input, union


@input
class CreateProductInput:
    sku: str
    name: str
    price: float
    brand: str


@input
class UpdateProductInput:
    sku: str
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@type
class CreateProductResponse:
    sku: str
    name: str
    price: float
    brand: str


@type
class UpdateProductResponse:
    name: str
    price: float
    brand: str


@type
class DeleteProductResponse:
    sku: str
    message: str


@type
class ProductError:
    message: str


CreateProductResult = union("CreateProductResult", (CreateProductResponse, ProductError))
UpdateProductResult = union("UpdateProductResult", (UpdateProductResponse, ProductError))
DeleteProductResult = union("DeleteProductResult", (DeleteProductResponse, ProductError))