import requests
from app.post_ms.posts.definitions.post import PostClass
from strawberry.exceptions import GraphQLError

def get_one_post(postId: str) -> PostClass:
    try:
        response = requests.get("http://localhost:3001/posts",headers={"PostId":f"{postId}"})
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))
        posts = response.json()
        cleaned_posts = []
        for post in posts:
            cleaned_post = {}
            for key, value in post.items():
                if key != '__v':
                    cleaned_post[key] = value
            cleaned_posts.append(cleaned_post)
        post_objects = [PostClass(**post) for post in cleaned_posts]
        return post_objects[0]
    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")
