import strawberry
import typing

@strawberry.type
class PostClass: #Aply to get_one_post
    _id: str
    Content: str
    Media: typing.List[str]
    GroupId: typing.Optional[str] = None
    UserId: str
    createdAt: str
    updatedAt:str

@strawberry.type # Aply to getuserPosts and getGroupPosts
class paginatedPosts:
    currentPage: int
    totalPages: int
    totalCount: int
    items: typing.List[PostClass] #TODO Procesar el __v
