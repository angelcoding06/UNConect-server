from app.auth_ms.auth.auth_schema import Query as AuthQuery
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.post_ms.posts.post_schema import Query as PostQuery
from app.post_ms.posts.post_schema import Mutation as PostMutation
from app.post_ms.likes.likes_schema import Query as LikeQuery
from app.post_ms.likes.likes_schema import Mutation as LikeMutation
from app.post_ms.comments.comments_schema import Query as CommentQuery
from app.post_ms.comments.comments_schema import Mutation as CommentMutation
from app.auth_ms.auth.auth_schema import Query as AuthQuery, Mutation as AuthMutation
# TODO fix the urls


@strawberry.type
class HelloQuery:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


@strawberry.type
class Query(HelloQuery, PostQuery, LikeQuery, CommentQuery, AuthQuery):
    pass


@strawberry.type
class Mutation(PostMutation, LikeMutation, CommentMutation, AuthMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Hello World from Api gateway"}


@strawberry.type
class HelloQuery:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
