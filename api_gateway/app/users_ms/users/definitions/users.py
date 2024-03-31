import strawberry
import typing
from datetime import date
@strawberry.type
class User:
	ID :str
	ID_Auth: str
	Name:str
	Last_Name:str
	Birthday:str
	Campus:str
	Faculty:str
	Career: str
	MemberUN_Since: int
	Phone_Number: str
	Gender: str
	Profile_Photo: str
	myGroups: typing.List[str]
	updatedAt: str
	createdAt: str

@strawberry.type
class FriendRequestClass:
	ID: str
	status: str
	senderId: str
	receiverId: str
	updatedAt: str
	createdAt: str 

@strawberry.type
class FriendsArray:
	friendIds: typing.List[str]
