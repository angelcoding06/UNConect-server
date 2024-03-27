import strawberry
import typing
from typing import Union
from app.posts.definitions.post import PostClass
from app.posts.post_resolvers import get_one_post
@strawberry.type
class error:
    statusCode:int
    message:str
@strawberry.type
class Query:
    onePost:Union[error,PostClass] = strawberry.field(resolver=get_one_post)
    
@strawberry.type
class Mutation:
    create_post: PostClass = ...

