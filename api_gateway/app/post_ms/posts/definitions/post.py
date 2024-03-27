import strawberry
import typing

@strawberry.type
class PostClass:
    _id: str
    Content: str
    Media: typing.List[str]
    UserId: str
    createdAt: str
    updatedAt:str
