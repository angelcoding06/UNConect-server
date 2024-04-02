import strawberry
import typing

@strawberry.type
class GrouppClass:
		id: int
		name: str
		photo: str
		description: str
		is_private: bool
		owner_id: int
		in_requests: typing.List[int]
		members: typing.List[int]
		admins: typing.List[int]

@strawberry.type
class GrouppClassResponse:
	groups:typing.List[GrouppClass]
@strawberry.type
class UserGroup:
		id: int
		user_id: str

@strawberry.type
class UserResponse:
	users:typing.List[UserGroup]



#getgroup = array de esto

# {
#         "id": 3,
#         "name": "Grupo de prueba2",
#         "photo": "1",
#         "description": "este grupo va a tratar de las enseñanzas de Roger a sus alumnos de ingles",
#         "is_private": false,
#         "owner_id": 4,
#         "in_requests": [],
#         "members": [
#             4,
#             5
#         ],
#         "admins": [
#             4,
#             5
#         ]
#     },
# # get in request, recibe un group id
# [
#     {
#         "id": 5,
#         "user_id": "123456789"
#     }
# ]

# # get members recibe un id de un grupo
# [
#     {
#         "id": 4,
#         "user_id": "22222222222222222"
#     },
#     {
#         "id": 5,
#         "user_id": "123456789"
#     }
# ]
# # get admins recibe un id de un grupo
# [
#     {
#         "id": 4,
#         "user_id": "22222222222222222"
#     },
#     {
#         "id": 5,
#         "user_id": "123456789"
#     }
# ]
# # get group by id trae el grupo con el id que se le pasa
# {
#     "id": 5,
#     "name": "Grupo de prueba2",
#     "photo": "1",
#     "description": "este grupo va a tratar de las enseñanzas de Roger a sus alumnos de ingles",
#     "is_private": true,
#     "owner_id": 4,
#     "in_requests": [],
#     "members": [
#         4,
#         5
#     ],
#     "admins": []
# }
