import strawberry
from app.group_ms.groups.definitions.group import GrouppClass,UserResponse,GrouppClassResponse
from app.group_ms.groups.group_resolver import get_groups,get_in_requests,get_members_by_group,get_admins_by_group,get_group,create_group,edit_group,delete_group,add_in_request,delete_in_request,add_user_to_group,delete_user_from_group,add_admin_to_group,delete_admin_from_group
import typing
@strawberry.type
class Query:
	getGroups: GrouppClassResponse = strawberry.field(resolver=get_groups)
	getInRequests: UserResponse = strawberry.field(resolver=get_in_requests)
	getMembersByGroup: UserResponse = strawberry.field(resolver=get_members_by_group)
	getAdminsByGroup: UserResponse = strawberry.field(resolver=get_admins_by_group)
	getGroup: GrouppClass = strawberry.field(resolver=get_group)
@strawberry.type
class Mutation:
	createGroup:GrouppClass = strawberry.field(resolver=create_group)
	editGroup:GrouppClass = strawberry.field(resolver=edit_group)
	deleteGroup: str = strawberry.field(resolver = delete_group)
	addInRequest: GrouppClass = strawberry.field(resolver=add_in_request)
	deleteInRequest : GrouppClass = strawberry.field(resolver=delete_in_request)
	addUserToGroup: GrouppClass = strawberry.field(resolver=add_user_to_group)
	deleteUserFromGroup: GrouppClass = strawberry.field(resolver=delete_user_from_group)
	addAdminToGroup: GrouppClass = strawberry.field(resolver=add_admin_to_group)
	deleteAdminFromGroup : GrouppClass = strawberry.field(resolver=delete_admin_from_group)
