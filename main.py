from fastapi import FastAPI, Depends, Header
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from config.environment import config_env
# from metadata.Tags import Tags
from config.database import get_db_connection
from models.base_model import init
from schemas.graphql.query import Query
from schemas.graphql.mutation import Mutation

# Application Environment Configuration
env = config_env()

# Core Application Instance
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    # openapi_tags=Tags,
)

#
# def authorization_dependency(
#     authorization: str = Header(None)
# ) -> str:
#     # ===> need to get request here, to get request header
#     return authorization


async def get_context(
    db=Depends(get_db_connection)
):
    return {
        "db": db,
    }


# GraphQL Schema and Application Instance
schema = Schema(
    query=Query,
    mutation=Mutation,

)

graphql = GraphQLRouter(
    schema,
    graphiql=env.DEBUG_MODE,
    context_getter=get_context,
)

# Integrate GraphQL Application to the Core one
app.include_router(
    graphql,
    prefix="/graphql",
    include_in_schema=False,
)

# Initialise Data Model Attributes
init()