import strawberry
from app.post_ms.posts.definitions.post import PostClass, paginatedPosts
from app.post_ms.posts.post_resolvers import get_one_post, get_user_posts, get_group_posts

@strawberry.type
class Query:
    getOnePost: PostClass = strawberry.field(resolver=get_one_post)
    getUserPosts: paginatedPosts = strawberry.field(resolver=get_user_posts)
    getGroupPosts: paginatedPosts = strawberry.field(resolver=get_group_posts)


@strawberry.type
class Mutation:
    createPost: PostClass = ...
    updatePost: PostClass = ...
    deletePost: str = ...

