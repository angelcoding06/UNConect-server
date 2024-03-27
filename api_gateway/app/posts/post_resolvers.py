import requests
import strawberry
import typing
from typing import Union
from app.posts.definitions.post import PostClass
from typing_extensions import Annotated
from strawberry.exceptions import GraphQLError

#6601c81136a42da5a173f9d0
@strawberry.type
class error:
    statusCode:int
    message:str

@strawberry.union
class responsex:
    unionerror: Union[error, PostClass]

def get_one_post(postId: str) -> Union[error, PostClass]:
    try:
        response = requests.get("http://unconnect_posts_ms:3001/posts",headers={"PostId":f"{postId}"})
        print("RESPONSE: ", response.text)
        if response.status_code != 200:
            return response.text
        posts = response.json()
        # posts = [{'_id': '6601c81136a42da5a173f9d0', 'Content': 'Prueba de post a eliminar', 'Media': [], 'UserId': '1', 'createdAt': '2024-03-25T18:53:05.716Z', 'updatedAt': '2024-03-25T18:53:05.716Z', "__v":0}]
        cleaned_posts = []
        for post in posts:
            cleaned_post = {}
            for key, value in post.items():
                if key != '__v':
                    cleaned_post[key] = value
            cleaned_posts.append(cleaned_post)
        post_objects = [PostClass(**post) for post in cleaned_posts]
        print(post_objects)
        return post_objects
    except ValueError as e:  # Captura errores de conversión a JSON
            raise GraphQLError(str(e))

    except requests.RequestException as e:  # Captura errores de red
        raise GraphQLError(f"Error al contactar la API REST: {e}")

    except KeyError as e:  # Captura errores de acceso a claves
        raise GraphQLError(f"Error al procesar la respuesta: {e}")
    # print("RESPONSEEEEEEE", response)
    # print("Response . text ",response.text)
    # print("Response . status code ",response.status_code)
    # if(response.status_code != 200):
    #     return response.text
    # print(posts)

