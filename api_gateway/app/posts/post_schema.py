import strawberry
from typing import List,Optional
import typing
import requests

@strawberry.type
class Post:
	id: str
	content:str
	userId:str
	groupId:Optional[str]
	media: Optional[typing.List[str]]

@strawberry.type
class Query:
    posts: List[Post] = ...

@strawberry.type
class Mutation:
    create_post: Post = ...

