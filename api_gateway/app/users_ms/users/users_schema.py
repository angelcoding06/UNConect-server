import strawberry
from app.users_ms.users.definitions.users import User,FriendRequestClass, FriendsArray
from app.users_ms.users.users_resolvers import get_users,get_one_user,create_user,edit_user,delete_user,create_friend_request, accept_friend_request, reject_friend_request, delete_friendship, get_friends_ids
import typing


@strawberry.type
class Query:
    getUsers: typing.List[User] = strawberry.field(resolver=get_users)
    getOneUSer: User = strawberry.field(resolver=get_one_user)
    getFriendsIds:FriendsArray = strawberry.field(resolver=get_friends_ids)


@strawberry.type
class Mutation:
    createUser: User = strawberry.field(resolver=create_user)
    editUser: User = strawberry.field(resolver=edit_user)
    deleteUser: str = strawberry.field(resolver=delete_user)
    createFriend:FriendRequestClass = strawberry.field(resolver=create_friend_request)
    acceptFriend: str = strawberry.field(resolver=accept_friend_request)
    rejectFriend: str = strawberry.field(resolver=reject_friend_request)
    deleteFriendship: str = strawberry.field(resolver=delete_friendship)
