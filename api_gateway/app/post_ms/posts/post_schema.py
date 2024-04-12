import strawberry
from app.post_ms.posts.definitions.post import PostClass, paginatedPosts
from app.post_ms.posts.post_resolvers import get_one_post, get_user_posts, get_group_posts, create_post, edit_post, delete_post,get_my_post,get_feed

@strawberry.type
class Query:
    getOnePost: PostClass = strawberry.field(resolver=get_one_post)
    getFeed: paginatedPosts = strawberry.field(resolver=get_feed)
    getUserPosts: paginatedPosts = strawberry.field(resolver=get_user_posts)
    getGroupPosts: paginatedPosts = strawberry.field(resolver=get_group_posts)
    getMyPosts: paginatedPosts = strawberry.field(resolver=get_my_post)
@strawberry.type
class Mutation:
    createPost: PostClass = strawberry.field(resolver=create_post) # Requiere validación
    updatePost: PostClass = strawberry.field(resolver=edit_post)# Requiere validación
    deletePost: str = strawberry.field(resolver=delete_post)# Requiere validación

