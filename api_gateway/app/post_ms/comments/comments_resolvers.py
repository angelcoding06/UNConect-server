import requests
from app.post_ms.comments.definitions.comments import CommentClass, paginatedComments
from strawberry.exceptions import GraphQLError
from app.const import POST_MS_URL
from app.utils.verifyuser import verifyUser
def get_comment_by_post(PostId:str,page:int) -> paginatedComments:
    try:
        response = requests.get(f"{POST_MS_URL}/comments/?page={page}",headers={"PostId":f"{PostId}"})
        print(response)
        print(response.json())
        print(response.text)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        for comment in json_response["items"]:
            comment.pop("__v")
            print("comment: ",comment)
        paginatedComment = paginatedComments(**json_response)
        paginatedComment.items = [CommentClass(**item) for item in json_response["items"]]
        return paginatedComment
    
    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")


def create_comment(token:str ,PostId:str, Content:str) -> CommentClass:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
        raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
        raise GraphQLError("Fallo al verificar")
    UserId = userVerified.id
    try:
        response = requests.post(f"{POST_MS_URL}/comments", headers = {"UserId":UserId, "PostId":PostId}, json = {"Content":Content})
        print(response.json())
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        json_response.pop('__v') # Increible
        return CommentClass(**json_response)

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")



def edit_comment(token:str ,PostId:str, Content:str, CommentId:str) -> CommentClass:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
        raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
        raise GraphQLError("Fallo al verificar")
    try:
        response = requests.patch(f"{POST_MS_URL}/comments", headers = {"CommentId":CommentId, "PostId": PostId}, json = {"Content":Content})
        print(response.json())
        if response.status_code != 200:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        json_response.pop('__v') 
        return CommentClass(**json_response)

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")
    
def delete_comment(token:str ,PostId:str, CommentId:str) -> str:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
        raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
        raise GraphQLError("Fallo al verificar")
    try:
        response = requests.delete(f"{POST_MS_URL}/comments", headers = {"PostId":PostId,"CommentId":CommentId})
        if response.status_code != 200:
            raise GraphQLError(str(response.json()))
        return response.text

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")
