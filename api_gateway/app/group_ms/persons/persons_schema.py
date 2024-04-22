import strawberry
from app.group_ms.persons.definitions.persons import PersonGroupClass, PersonGroupResponse
from app.group_ms.persons.persons_resolvers import get_person_group,create_person_group,edit_person_group,delete_person_group,get_person_g_by_auth_id
import typing
@strawberry.type
class Query:
    GetPersonss: PersonGroupResponse = strawberry.field(resolver=get_person_group)
    PersonByAuthID: PersonGroupClass = strawberry.field(resolver=get_person_g_by_auth_id)


@strawberry.type
class Mutation:
    createPersonGroup: PersonGroupClass = strawberry.field(resolver=create_person_group)
    updatePersonGroup: PersonGroupClass = strawberry.field(resolver=edit_person_group)
    deletePersonGroup: str = strawberry.field(resolver=delete_person_group)
