import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.post_ms.posts.post_schema import Query as PostQuery

@strawberry.type
class HelloQuery:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
    
@strawberry.type
class Query(HelloQuery,PostQuery):
    pass

schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Hello World from Api gateway"}


