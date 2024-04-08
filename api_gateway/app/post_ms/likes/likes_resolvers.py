import requests
from app.post_ms.likes.definitions.likes import LikesClass, paginatedLikes
from strawberry.exceptions import GraphQLError
from app.const import POST_MS_URL
from app.utils.verifyuser import verifyUser
def get_like_by_post(PostId:str,page:int) -> paginatedLikes:
    try:
        response = requests.get(f"{POST_MS_URL}/likes?page={page}",headers={"PostId":f"{PostId}"})
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        for like in json_response["items"]:
            like.pop("__v")
        paginatedLike = paginatedLikes(**json_response)
        paginatedLike.items = [LikesClass(**item) for item in json_response["items"]]
        return paginatedLike
    
    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def create_like(token:str ,PostId:str, type:str) -> LikesClass:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
        raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
        raise GraphQLError("Fallo al verificar")
    UserId = userVerified.id
    try:
        response = requests.post(f"{POST_MS_URL}/likes", headers = {"UserId":UserId, "PostId":PostId}, json = {"type":type})
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        json_response.pop('__v') # Increible
        return LikesClass(**json_response)

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")



def edit_like(token:str ,PostId:str, type:str) -> LikesClass:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
        raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
        raise GraphQLError("Fallo al verificar")
    UserId = userVerified.id
    try:
        response = requests.patch(f"{POST_MS_URL}/likes", headers = {"UserId":UserId, "PostId": PostId}, json = {"type":type})
        if response.status_code != 200:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        json_response.pop('__v') 
        return LikesClass(**json_response)

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")
    
def delete_like(token:str ,PostId:str) -> str:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
        raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
        raise GraphQLError("Fallo al verificar")
    UserId = userVerified.id
    try:
        response = requests.delete(f"{POST_MS_URL}/likes", headers = {"PostId":PostId,"UserId":UserId})
        if response.status_code != 200:
            raise GraphQLError(str(response.json()))
        return response.text

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")
