import strawberry
import typing
from enum import Enum


@strawberry.enum
class Role(Enum):
    ADMIN = "admin"
    USUARIO_REGULAR = "usuario_regular"
    MODERADOR = "moderador"
    SUPERUSUARIO = "SUPERUSUARIO"


@strawberry.type
class AuthClass:  # Aply to get_one_post
    id: str
    email: str
    isVerified: bool
    role: Role


@strawberry.type
class TokenClass:
    token: str
