from strawberry import type

from gql.mutation.auth import MutationAuth
from gql.mutation.product import MutationProduct
from gql.mutation.user import MutationUser


@type
class Mutation(MutationAuth, MutationProduct, MutationUser):
    pass
