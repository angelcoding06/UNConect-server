import strawberry
from app.group_ms.persons.definitions.persons import PersonGroupClass, PersonGroupResponse
from app.group_ms.persons.persons_resolvers import get_person_group,create_person_group,edit_person_group,delete_person_group
import typing
@strawberry.type
class Query:
    PersonGroupClass: PersonGroupResponse = strawberry.field(resolver=get_person_group)


@strawberry.type
class Mutation:
    createPersonGroup: PersonGroupClass = strawberry.field(resolver=create_person_group)
    updatePersonGroup: PersonGroupClass = strawberry.field(resolver=edit_person_group)
    deletePersonGroup: str = strawberry.field(resolver=delete_person_group)
