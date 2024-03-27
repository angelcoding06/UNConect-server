import strawberry
from app.post_ms.posts.definitions.post import PostClass
from app.post_ms.posts.post_resolvers import get_one_post

@strawberry.type
class Query:
    getOnePost: PostClass = strawberry.field(resolver=get_one_post)
    
@strawberry.type
class Mutation:
    create_post: PostClass = ...

