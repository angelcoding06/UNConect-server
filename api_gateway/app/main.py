from typing import Union
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.posts.post_resolvers import Query as PostQuery


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
    @strawberry.field
    def bye(self) -> str:
        return "bye World"
    
@strawberry.type
class Query(PostQuery):
    pass
schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Hello World"}


