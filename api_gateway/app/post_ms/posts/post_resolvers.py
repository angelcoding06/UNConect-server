import requests
from app.post_ms.posts.definitions.post import PostClass, paginatedPosts
from strawberry.exceptions import GraphQLError
from app.const import POST_MS_URL
import typing
from app.utils.verifyuser import verifyUser
def get_one_post(postId: str) -> PostClass:
    try:
        response = requests.get(f"{POST_MS_URL}/posts",headers={"PostId":f"{postId}"})
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        post=json_response[0]
        post.pop("__v")
        return PostClass(**post)

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")

def get_user_posts(UserId:str, page: int, GroupId:str = None)-> paginatedPosts:
    if GroupId is None:
        headers={"UserId":f"{UserId}"}
    else:
        headers={"UserId":f"{UserId}","GroupId":f"{GroupId}"}
    try:
        response = requests.get(f"{POST_MS_URL}/posts/userPost?page={page}",headers=headers)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        for post in json_response["items"]:
            post.pop("__v")
        paginatedPost = paginatedPosts(**json_response)
        paginatedPost.items = [PostClass(**item) for item in json_response["items"]]
        return paginatedPost
    
    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")

def get_group_posts(page: int, GroupId:str)-> paginatedPosts:
    try:
        response = requests.get(f"{POST_MS_URL}/posts/groupPost?page={page}",headers={"GroupId":f"{GroupId}"})
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        for post in json_response["items"]:
            post.pop("__v")
        paginatedPost = paginatedPosts(**json_response)
        paginatedPost.items = [PostClass(**item) for item in json_response["items"]]
        return paginatedPost

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")

def create_post(token:str, Content:str, GroupId:str = None, Media: typing.List[str] = [])-> PostClass:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
      raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
      raise GraphQLError("Fallo al verificar")
    UserId = userVerified.id
    if GroupId is None:
        headers={"UserId":f"{UserId}"}
    else:
        headers={"UserId":f"{UserId}","GroupId":f"{GroupId}"}
    try:
        response = requests.post(f"{POST_MS_URL}/posts/", headers = headers, json = {"Content":Content, "Media":Media})
        print(response.json())
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        json_response.pop('__v') # Increible
        return PostClass(**json_response)

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")

def edit_post(Content:str, PostId:str, token:str, GroupId:str = None)-> PostClass:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
      raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
      raise GraphQLError("Fallo al verificar")
    if GroupId is None:
        headers={"PostId":f"{PostId}"}
    else:
        headers={"PostId":f"{PostId}","GroupId":f"{GroupId}"}
    try:
        response = requests.patch(f"{POST_MS_URL}/posts", headers = headers, json = {"Content":Content})
        print(response.json())
        if response.status_code != 200:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        json_response.pop('__v') 
        return PostClass(**json_response)

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")

def delete_post(PostId:str, token:str)-> str:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
      raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
      raise GraphQLError("Fallo al verificar")
    try:
        response = requests.delete(f"{POST_MS_URL}/posts", headers = {"PostId":f"{PostId}"})
        if response.status_code != 200:
            raise GraphQLError(str(response.json()))
        return response.text

    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")

def get_my_post(token:str, page: int, GroupId:str = None)-> paginatedPosts:
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
        raise GraphQLError("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
        raise GraphQLError("Fallo al verificar")
    UserId = userVerified.id
    if GroupId is None:
        headers={"UserId":f"{UserId}"}
    else:
        headers={"UserId":f"{UserId}","GroupId":f"{GroupId}"}
    try:
        response = requests.get(f"{POST_MS_URL}/posts/userPost?page={page}",headers=headers)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        json_response = response.json()
        for post in json_response["items"]:
            post.pop("__v")
        paginatedPost = paginatedPosts(**json_response)
        paginatedPost.items = [PostClass(**item) for item in json_response["items"]]
        return paginatedPost
    
    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")
