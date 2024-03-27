import requests
from app.post_ms.posts.definitions.post import PostClass, paginatedPosts
from strawberry.exceptions import GraphQLError
from app.post_ms.const import POST_MS_URL
def get_one_post(postId: str) -> PostClass:
    try:
        response = requests.get(f"{POST_MS_URL}/posts",headers={"PostId":f"{postId}"})
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

def get_user_posts(UserId:str, page: int, GroupId:str = None)-> paginatedPosts:
    if GroupId is None:
        headers={"UserId":f"{UserId}"}
    else:
        headers={"UserId":f"{UserId}","GroupId":f"{GroupId}"}

    try:
        response = requests.get(f"http://localhost:3001/posts/userPost?page={page}",headers=headers)
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))

        posts = response.json()
        post = paginatedPosts(**posts)

        cleaned_posts = []
        for item in posts['items']:
            cleaned_item = {k: v for k, v in item.items() if k != '__v'}
            cleaned_posts.append(cleaned_item)

        post.items = [PostClass(**item) for item in cleaned_posts]

        return post
    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")

def get_group_posts(page: int, GroupId:str)-> paginatedPosts:
    try:
        response = requests.get(f"http://localhost:3001/posts/groupPost?page={page}",headers={"GroupId":f"{GroupId}"})
        if response.status_code == 404:
            raise GraphQLError(str(response.json()))

        posts = response.json()
        post = paginatedPosts(**posts)

        cleaned_posts = []
        for item in posts['items']:
            cleaned_item = {k: v for k, v in item.items() if k != '__v'}
            cleaned_posts.append(cleaned_item)

        post.items = [PostClass(**item) for item in cleaned_posts]

        return post
    except ValueError as error: # Bad format
        raise GraphQLError(str(error))
    except requests.RequestException as error:  # net errors
        raise GraphQLError(f"Error al contactar la API REST: {error}")
    except KeyError as error:  # Keys error
        raise GraphQLError(f"Error al procesar la respuesta: {error}")

def create_post(Content:str, Media: list, UserId:str, GroupId:str = None)-> PostClass:
    pass
