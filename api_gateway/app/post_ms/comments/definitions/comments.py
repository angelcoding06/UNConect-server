import strawberry
import typing

@strawberry.type
class CommentClass: 
    _id: str
    Content: str
    UserId: str
    PostId: str
    createdAt: str
    updatedAt:str

@strawberry.type
class paginatedComments:
    currentPage: int
    totalPages: int
    totalCount: int
    items: typing.List[CommentClass]

