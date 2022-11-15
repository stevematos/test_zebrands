#!/usr/bin/env python
from config.database import get_db_connection, init
from config.environment import API_VERSION, APP_NAME, DEBUG_MODE
from fastapi import Depends, FastAPI, Header
from gql.mutation import Mutation
from gql.query import Query
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

# Core Application Instance
app = FastAPI(
    title=APP_NAME,
    version=API_VERSION,
)


def authorization_dependency(session_token: str = Header(None)) -> str:
    return session_token


async def get_context(
    db=Depends(get_db_connection),
    session_token=Depends(authorization_dependency),
):
    return {"db": db, "session_token": session_token}


# GraphQL Schema and Application Instance
schema = Schema(
    query=Query,
    mutation=Mutation,
)

graphql = GraphQLRouter(
    schema,
    graphiql=DEBUG_MODE,
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
