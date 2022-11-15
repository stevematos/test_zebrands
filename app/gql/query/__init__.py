from gql.query.product import QueryProduct
from strawberry.tools import merge_types

Query = merge_types("Query", (QueryProduct,))
