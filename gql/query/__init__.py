from strawberry.tools import merge_types


from gql.query.product import QueryProduct

Query = merge_types("Query", (QueryProduct,))
