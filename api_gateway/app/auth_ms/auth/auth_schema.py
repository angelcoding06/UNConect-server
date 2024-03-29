import strawberry
from app.auth_ms.auth.definitions.auth import AuthClass, TokenClass
from app.auth_ms.auth.auth_resolvers import get_auth_user, login, register, validate, update, partial_update, delete


@strawberry.type
class Query:
    getAuthUser: AuthClass = strawberry.field(resolver=get_auth_user)
    # metodos get


@strawberry.type
class Mutation:
    createAuthUser: AuthClass = strawberry.field(resolver=register)
    validateAuthUser: AuthClass = strawberry.field(resolver=validate)
    loginAuthUser: TokenClass = strawberry.field(resolver=login)
    updateAuthUser = strawberry.field(resolver=update)
    partialUpdateAuthUser = strawberry.field(resolver=partial_update)
    deleteAuthUser = strawberry.field(resolver=delete)
    # metodos post, update, delete, etc
