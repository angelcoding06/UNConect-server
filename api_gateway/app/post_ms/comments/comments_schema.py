import strawberry
from app.post_ms.comments.definitions.comments import CommentClass, paginatedComments
from app.post_ms.comments.comments_resolvers import get_comment_by_post, create_comment, edit_comment, delete_comment

@strawberry.type
class Query:
    getcommentbyPost: paginatedComments = strawberry.field(resolver=get_comment_by_post)

@strawberry.type
class Mutation:
    createcomment: CommentClass = strawberry.field(resolver=create_comment)
    updatecomment: CommentClass = strawberry.field(resolver=edit_comment)
    deletecomment: str = strawberry.field(resolver=delete_comment)

