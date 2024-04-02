import strawberry
import typing
from enum import Enum


@strawberry.enum
class Role(Enum):
    ADMIN = "ADMIN"
    USUARIO_REGULAR = "USUARIO_REGULAR"
    MODERADOR = "MODERADOR"
    SUPERUSUARIO = "SUPERUSUARIO"


@strawberry.type
class AuthClass:  # Aply to get_one_post
    id: str
    email: str
    verified: bool
    role: Role


@strawberry.type
class TokenClass:
    token: str
