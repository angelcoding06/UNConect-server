import strawberry
from app.post_ms.likes.definitions.likes import LikesClass, paginatedLikes
from app.post_ms.likes.likes_resolvers import get_like_by_post, create_like, edit_like, delete_like

@strawberry.type
class Query:
    getLikebyPost: paginatedLikes = strawberry.field(resolver=get_like_by_post)

@strawberry.type
class Mutation:
    createLike: LikesClass = strawberry.field(resolver=create_like) # Requiere validación
    updateLike: LikesClass = strawberry.field(resolver=edit_like) # Requiere validación 
    deleteLike: str = strawberry.field(resolver=delete_like)# Requiere validación

