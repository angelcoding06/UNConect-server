import strawberry
import typing

@strawberry.type
class LikesClass: 
    _id: str
    type: str
    UserId: str
    PostId: str
    createdAt: str
    updatedAt:str

@strawberry.type
class paginatedLikes:
    currentPage: int
    totalPages: int
    totalCount: int
    items: typing.List[LikesClass]

