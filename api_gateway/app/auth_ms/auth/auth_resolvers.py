import requests
from app.auth_ms.auth.definitions.auth import AuthClass, TokenClass, Role
from strawberry.exceptions import GraphQLError
from app.auth_ms.const import AUTH_MS_URL
from typing import Optional

URL = f"{AUTH_MS_URL}/auth/"


def get_auth_user(id: str) -> AuthClass:
    try:
        response = requests.get(
            f"{URL}/{id}")
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        auth_user = response.json()

        return auth_user
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def login(email: str, password: str) -> TokenClass:
    try:
        json_obj = {email, password}
        response = requests.post(f"{URL}/login", json_obj)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        token = response.json()

        return token
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def register(email: str, password: str, role: Role) -> TokenClass:
    try:
        json_obj = {email, password, role}
        response = requests.post(f"{URL}", json_obj)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        token = response.json()

        return token
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def validate(token: str) -> AuthClass:
    try:
        json_obj = {token}
        response = requests.post(f"{URL}/validate", json_obj)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        token = response.json()

        return token
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def update(email: str, password: str, verified: bool, role: Role, id: str) -> AuthClass:
    try:
        json_obj = {email, password, verified, role}
        response = requests.put(f"{URL}/{id}", json_obj)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        token = response.json()

        return token
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def partial_update(id: str, email: Optional[str] = None, password: Optional[str] = None, verified: Optional[str] = None, role: Optional[Role] = None) -> AuthClass:
    try:
        json_obj = {email, password, verified, role}
        response = requests.patch(f"{URL}/{id}", json_obj)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        token = response.json()

        return token
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def delete(id: str) -> AuthClass:
    try:
        response = requests.delete(f"{URL}/{id}")
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        token = response.json()

        return token
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")
