import strawberry
from app.users_ms.users.definitions.users import User,FriendRequestClass, FriendsArray,UserFriendships
from app.users_ms.users.users_resolvers import get_users,get_one_user,edit_user,delete_user,create_friend_request, accept_friend_request, reject_friend_request, delete_friendship, get_friends_ids,get_user_by_auth_id,get_user_friendships
import typing


@strawberry.type
class Query:
    getUsers: typing.List[User] = strawberry.field(resolver=get_users) #Puede que no se use
    getOneUSer: User = strawberry.field(resolver=get_one_user) # Puede que no se use 
    getUserByAuthId: User = strawberry.field(resolver=get_user_by_auth_id) # Lista validación
    getFriendsIds:FriendsArray = strawberry.field(resolver=get_friends_ids) # Lista validación
    getUserFriendships: UserFriendships = strawberry.field(resolver=get_user_friendships) # Lista validación

@strawberry.type
class Mutation:
    # createUser: User = strawberry.field(resolver=create_user) Ya no se usa
    editUser: User = strawberry.field(resolver=edit_user) # Lista validación
    deleteUser: str = strawberry.field(resolver=delete_user) # Lista validación
    createFriend:FriendRequestClass = strawberry.field(resolver=create_friend_request) # Lista validación
    acceptFriend: str = strawberry.field(resolver=accept_friend_request) # Lista validación
    rejectFriend: str = strawberry.field(resolver=reject_friend_request) # Lista validación
    deleteFriendship: str = strawberry.field(resolver=delete_friendship) # Lista validación
