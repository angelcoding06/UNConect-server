import strawberry
import typing
@strawberry.type
class PersonGroupClass:
    id: str
    user_id: str

@strawberry.type
class Person:
	user_id:str

@strawberry.type
class PersonGroupResponse:
	persons: typing.List[PersonGroupClass]

@strawberry.type
class groupclass:
	id:str
	name:str
	photo:str
	description:str
	is_private:bool
	owner_id:int
	in_requests: typing.List[int]
	members: typing.List[int]
	admins: typing.List[int]
