import requests
from app.auth_ms.auth.definitions.auth import AuthClass, TokenClass, Role
from strawberry.exceptions import GraphQLError
from app.auth_ms.const import AUTH_MS_URL
from typing import Optional
import json
URL = f"{AUTH_MS_URL}/auth"


def jsonToAuthClass(json) -> AuthClass:
    auth = AuthClass(**json)
    auth.role = Role(auth.role)
    return auth


def get_auth_user(id: str) -> AuthClass:
    try:
        response = requests.get(
            f"{URL}/{id}")
        if response.status_code == 404:
            raise GraphQLError(str("User not existing"))
        auth_user = response.json()
        return jsonToAuthClass(auth_user)
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def login(email: str, password: str) -> TokenClass:
    try:
        json_obj = {"email": email, "password": password}
        response = requests.post(f"{URL}/login", json=json_obj)
        print(response.status_code)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        token = response.json()
        print(token)
        return TokenClass(**token)
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def register(email: str, password: str, role: Role) -> AuthClass:

    try:
        json_obj = {"email": email,  "role": role.name,"password": password}

        response = requests.post(f"{URL}", json=json_obj)

        if response.status_code != 200:
            raise GraphQLError(str(response.text))

        data = response.text
        data = json.loads(data)
        auth = AuthClass(**data)
        auth.role = Role[auth.role]
        return auth
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def validate(token: str) -> AuthClass:
    try:
        response = requests.post(f"{URL}/validate?token={token}")
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        auth = response.json()
        print(auth)
        return jsonToAuthClass(auth)
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def update(email: str, password: str, verified: bool, role: Role, id: str) -> str:
    try:
        json_obj = {"email": email, "password": password,
                    "role": role.name, "verified": verified}
        response = requests.put(f"{URL}/{id}", json=json_obj)
        print(response.status_code)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        if response.status_code == 200:
            return "satisfactory update"
        return ""
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def partial_update(id: str, email: Optional[str] = None, password: Optional[str] = None, verified: Optional[bool] = None, role: Optional[Role] = None) -> AuthClass:
    try:
        json_obj = {"email": email, "password": password,
                    "role": role.name, "verified": verified}
        response = requests.patch(f"{URL}/{id}", json=json_obj)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        auth = response.json()

        return jsonToAuthClass(auth)
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def delete(id: str) -> str:
    try:
        response = requests.delete(f"{URL}/{id}")
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        if response.status_code == 200:
            return "satisfactory delete"
        return ""
    except ValueError as error:  # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")
