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
