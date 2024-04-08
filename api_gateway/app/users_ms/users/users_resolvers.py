from  datetime import date
import requests
from app.users_ms.users.definitions.users import User,FriendRequestClass, FriendsArray,UserFriendships
from strawberry.exceptions import GraphQLError
from app.const import USER_MS_URL
import typing
import json
from app.utils.verifyuser import verifyUser
def get_users() -> typing.List[User]:
		try:
				response = requests.get(f"{USER_MS_URL}/users")
				if response.status_code == 404:
					raise GraphQLError(str(response.json()))
				jsonresponse=response.json()
				if len(jsonresponse) == 0:
					raise GraphQLError("NO USERS FOUND")
				response=[]
				for user in jsonresponse:
					user = User(**user)
					response.append(user)
				return response
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def get_one_user(userId:str) -> User:
		try:
				response = requests.get(f"{USER_MS_URL}/users/{userId}")
				print(response)
				if response.status_code != 200:
					raise GraphQLError(response.text)
				jsonresponse=response.json()
				print(jsonresponse)
				jsonresponse = User(**jsonresponse)
				return jsonresponse
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

# def create_user(ID_Auth: str,Name:str,Last_Name:str,Birthday:str,Campus:str,Faculty:str,Career: str,MemberUN_Since: int,Phone_Number: str,Gender: str,Profile_Photo: str,myGroups: typing.List[str])-> User:
# 	jsonobject = {"ID_Auth":ID_Auth,"Name":Name,"Last_Name":Last_Name,"Birthday":Birthday,"Campus":Campus,"Faculty":Faculty,"Career":Career,"MemberUN_Since":MemberUN_Since,"Phone_Number" :Phone_Number, "Gender":Gender,"Profile_Photo":Profile_Photo,"myGroups":myGroups}
# 	try:
# 		response = requests.post(f"{USER_MS_URL}/users/", json = jsonobject)
# 		print(response.json())
# 		if response.status_code != 201:
# 			raise GraphQLError(str(response.text))
# 		json_response = response.json()
# 		return User(**json_response)
	
# 	except ValueError as error: # Bad format
# 		raise GraphQLError(str(error))
# 	except requests.RequestException as error:  # net errors
# 		raise GraphQLError(f"Error al contactar la API REST: {error}")
# 	except KeyError as error:  # Keys error
# 		raise GraphQLError(f"Error al procesar la respuesta: {error}")

def edit_user(
		token: str,
		Name: typing.Optional[str] = None,
		Last_Name: typing.Optional[str] = None,
		Birthday: typing.Optional[str] = None,
		Campus: typing.Optional[str] = None,
		Faculty: typing.Optional[str] = None,
		Career: typing.Optional[str] = None,
		MemberUN_Since: typing.Optional[int] = None,
		Phone_Number: typing.Optional[str] = None,
		Gender: typing.Optional[str] = None,
		Profile_Photo: typing.Optional[str] = None,
		myGroups: typing.Optional[typing.List[typing.Optional[str]]] = None
) -> User:
	#Esto es una mierda pero es todo lo que hay
		jsonobject = {}
		if Name is not None:
				jsonobject["Name"] = Name
		if Last_Name is not None:
				jsonobject["Last_Name"] = Last_Name
		if Birthday is not None:
				jsonobject["Birthday"] = Birthday
		if Campus is not None:
				jsonobject["Campus"] = Campus
		if Faculty is not None:
				jsonobject["Faculty"] = Faculty
		if Career is not None:
				jsonobject["Career"] = Career
		if MemberUN_Since is not None:
				jsonobject["MemberUN_Since"] = MemberUN_Since
		if Phone_Number is not None:
				jsonobject["Phone_Number"] = Phone_Number
		if Gender is not None:
				jsonobject["Gender"] = Gender
		if Profile_Photo is not None:
				jsonobject["Profile_Photo"] = Profile_Photo
		if myGroups is not None:
				jsonobject["myGroups"] = myGroups

		userVerified = verifyUser(token)
		if userVerified == "UNAUTHORIZED":
			raise GraphQLError("UNAUTHORIZED")
		if userVerified == "Fallo al verificar":
			raise GraphQLError("Fallo al verificar")
		userId = userVerified.id
		try:
				response = requests.put(f"{USER_MS_URL}/users/{userId}", json=jsonobject)
				print(response.json())
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.json()
				return User(**json_response)
		
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def delete_user(token:str)->str:
	userVerified = verifyUser(token)
	if userVerified == "UNAUTHORIZED":
		raise GraphQLError("UNAUTHORIZED")
	if userVerified == "Fallo al verificar":
		raise GraphQLError("Fallo al verificar")
	userId = userVerified.id
	try:
		response = requests.delete(f"{USER_MS_URL}/users/{userId}")
		if response.status_code != 200:
			raise GraphQLError(str(response.text))
		json=response.json()
		return json["message"]
	except ValueError as error: # Bad format
		raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
		raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
		raise GraphQLError(f"Error al procesar la respuesta: {error}")

def create_friend_request(token:str, receiverId:str)-> FriendRequestClass:
	userVerified = verifyUser(token)
	if userVerified == "UNAUTHORIZED":
		raise GraphQLError("UNAUTHORIZED")
	if userVerified == "Fallo al verificar":
		raise GraphQLError("Fallo al verificar")
	senderId = userVerified.id
	try:
		response = requests.post(f"{USER_MS_URL}/friends/",json={"senderId":senderId,"receiverId":receiverId})
		if response.status_code != 201:
			raise GraphQLError(str(response.text))
		json_response = response.json()
		return FriendRequestClass(**json_response)
	except ValueError as error: # Bad format
		raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
		raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
		raise GraphQLError(f"Error al procesar la respuesta: {error}")

def accept_friend_request(senderId:str, token:str)-> str:
	userVerified = verifyUser(token)
	if userVerified == "UNAUTHORIZED":
		raise GraphQLError("UNAUTHORIZED")
	if userVerified == "Fallo al verificar":
		raise GraphQLError("Fallo al verificar")
	receiverId = userVerified.id
	try:
		response = requests.put(f"{USER_MS_URL}/friends/accept/",json={"senderId":senderId,"receiverId":receiverId})
		if response.status_code != 200:
			raise GraphQLError(str(response.json()["message"]))
		json_response = response.json()
		return json_response["message"]
	except ValueError as error: # Bad format
		raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
		raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
		raise GraphQLError(f"Error al procesar la respuesta: {error}")

def reject_friend_request(senderId:str, token:str)-> str:
	userVerified = verifyUser(token)
	if userVerified == "UNAUTHORIZED":
		raise GraphQLError("UNAUTHORIZED")
	if userVerified == "Fallo al verificar":
		raise GraphQLError("Fallo al verificar")
	receiverId = userVerified.id
	try:
		response = requests.put(f"{USER_MS_URL}/friends/reject/",json={"senderId":senderId,"receiverId":receiverId})
		if response.status_code != 200:
			raise GraphQLError(str(response.json()["message"]))
		json_response = response.json()
		return json_response["message"]
	except ValueError as error: # Bad format
		raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
		raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
		raise GraphQLError(f"Error al procesar la respuesta: {error}")

def delete_friendship(token:str,friendshipId:str)-> str:
		userVerified = verifyUser(token)
		if userVerified == "UNAUTHORIZED":
			raise GraphQLError("UNAUTHORIZED")
		if userVerified == "Fallo al verificar":
			raise GraphQLError("Fallo al verificar")
		try:
			response = requests.delete(f"{USER_MS_URL}/friends/{friendshipId}/")
			if response.status_code != 200:
				raise GraphQLError(str(response.json()["message"]))
			json_response = response.json()
			return json_response["message"]
		except ValueError as error: # Bad format
			raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
			raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
			raise GraphQLError(f"Error al procesar la respuesta: {error}")
	
def get_friends_ids(token:str)->FriendsArray :
		userVerified = verifyUser(token)
		if userVerified == "UNAUTHORIZED":
			raise GraphQLError("UNAUTHORIZED")
		if userVerified == "Fallo al verificar":
			raise GraphQLError("Fallo al verificar")
		userId = userVerified.id
		try:
			response = requests.get(f"{USER_MS_URL}/friends/{userId}/")
			if response.status_code != 200:
				raise GraphQLError(str(response.json()["message"]))
			json_response = response.json()
			print("JSON RESPONSE : ",json_response)
			friends_ids = FriendsArray(**json_response)
			print("FRIENDS IDS",friends_ids)
			return friends_ids
		except ValueError as error: # Bad format
			raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
			raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
			raise GraphQLError(f"Error al procesar la respuesta: {error}")

def get_user_by_auth_id(token:str)->User:
		userVerified = verifyUser(token)
		if userVerified == "UNAUTHORIZED":
			raise GraphQLError("UNAUTHORIZED")
		if userVerified == "Fallo al verificar":
			raise GraphQLError("Fallo al verificar")
		id = userVerified.id

		try:
				response = requests.get(f"{USER_MS_URL}/users/authid/{id}")
				print(response)
				if response.status_code != 200:
					raise GraphQLError(response.text)
				jsonresponse=response.json()
				print(jsonresponse)
				jsonresponse = User(**jsonresponse)
				return jsonresponse
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")
		
def get_user_friendships(token:str)->UserFriendships:
		userVerified = verifyUser(token)
		if userVerified == "UNAUTHORIZED":
			raise GraphQLError("UNAUTHORIZED")
		if userVerified == "Fallo al verificar":
			raise GraphQLError("Fallo al verificar")
		UserID = userVerified.id

		try:
				response = requests.get(f"{USER_MS_URL}/friends/userfriendships/{UserID}")
				if response.status_code != 200:
						raise GraphQLError(response.text)
				print("RESPONSEEEEEEEEEE,",response)
				print("JSON",response.json())
				data = response.json()
				ids = data['friendships']
				finaldata=[]
				for friendship in ids:
					friendship = FriendRequestClass(**friendship)
					finaldata.append(friendship)
					print("Friendhips id: ",friendship)
				print(ids)
				print(UserFriendships(friendships=finaldata))
				return UserFriendships(friendships=finaldata)
		
		except ValueError as error:  # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")
