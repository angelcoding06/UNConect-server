import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.post_ms.posts.post_schema import Query as PostQuery
from app.post_ms.posts.post_schema import Mutation as PostMutation
from app.post_ms.likes.likes_schema import Query as LikeQuery
from app.post_ms.likes.likes_schema import Mutation as LikeMutation

@strawberry.type
class HelloQuery:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
    
@strawberry.type
class Query(HelloQuery,PostQuery,LikeQuery):
    pass

@strawberry.type
class Mutation(PostMutation,LikeMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Hello World from Api gateway"}


