from app.auth_ms.auth.auth_schema import Query as AuthQuery
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI,UploadFile, HTTPException
from fastapi.responses import StreamingResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import typing
import requests
from app.utils.verifyuser import verifyUser
from app.post_ms.posts.post_schema import Query as PostQuery
from app.post_ms.posts.post_schema import Mutation as PostMutation
from app.post_ms.likes.likes_schema import Query as LikeQuery
from app.post_ms.likes.likes_schema import Mutation as LikeMutation
from app.post_ms.comments.comments_schema import Query as CommentQuery
from app.post_ms.comments.comments_schema import Mutation as CommentMutation
from app.auth_ms.auth.auth_schema import Mutation as AuthMutation
from app.group_ms.persons.persons_schema import Query as PersonQuery
from app.group_ms.persons.persons_schema import Mutation as PersonMutation
from app.group_ms.groups.group_schema import Query as GroupQuery
from app.group_ms.groups.group_schema import Mutation as GroupMutation
from app.users_ms.users.users_schema import Query as UserQuery
from app.users_ms.users.users_schema import Mutation as UserMutation
from app.const import MEDIA_MS_URL
# TODO fix the urls


@strawberry.type
class HelloQuery:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


@strawberry.type
class Query(HelloQuery, PostQuery, LikeQuery, CommentQuery, AuthQuery,PersonQuery,UserQuery,GroupQuery):
    pass


@strawberry.type
class Mutation(PostMutation, LikeMutation, CommentMutation, AuthMutation,PersonMutation,UserMutation,GroupMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World from Api gateway"}


@app.post("/upload-file/") 
def upload_file(files: typing.List[UploadFile],token:str):
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
        raise HTTPException("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
        raise HTTPException("Fallo al verificar")
    UserId = userVerified.id
    print(files)
    files_data = []
    for file in files:
        file_data = ("files", (file.filename, file.file.read(), file.content_type))
        files_data.append(file_data)

    response = requests.post(f"{MEDIA_MS_URL}/media/file", files=files_data, headers={"UserId": UserId})
    print(response)
    print(response.text)
    print(response.json())
    ids=response.json()
    if response.status_code == 201:
        return JSONResponse(content={"message": "Files uploaded successfully", "ids": ids})
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to upload files")
    
@app.get("/get-file/") 
def get_file(file_id: str):
    response = requests.get(f"{MEDIA_MS_URL}/media/{file_id}")
    if response.status_code == 200:
        return StreamingResponse(io.BytesIO(response.content))
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch file")
    
@app.delete("/delete-file/") # Requiere validación
def delete_file(file_id: str, token:str):
    userVerified = verifyUser(token)
    if userVerified == "UNAUTHORIZED":
        raise HTTPException("UNAUTHORIZED")
    if userVerified == "Fallo al verificar":
        raise HTTPException("Fallo al verificar")
    response = requests.delete(f"{MEDIA_MS_URL}/media/{file_id}")
    if response.status_code == 200:
        return JSONResponse(content={"message": "File deleted successfully"})
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to delete file")
    
@app.get("/getmedia/")
def getmedia():
    response= requests.get(f"{MEDIA_MS_URL}")
    print(response)
