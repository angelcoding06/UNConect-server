import requests
from app.group_ms.groups.definitions.group import GrouppClass,UserResponse,GrouppClassResponse,UserGroup
from strawberry.exceptions import GraphQLError
from app.const import GROUP_MS_URL
import typing
import json



def get_groups() -> GrouppClassResponse:
		try:
				response = requests.get(f"{GROUP_MS_URL}/groups/getGroup/")
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response=json.loads(json_response)
				groups_response = []
				for group in json_response:
					groups_response.append(GrouppClass(**group))
				groups_response=GrouppClassResponse(groups=groups_response)
				return groups_response
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def get_in_requests(groupId:int)-> UserResponse:
		try:
				response = requests.get(f"{GROUP_MS_URL}/groups/get_in_request/{groupId}/")
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response=json.loads(json_response)
				users = []
				for user in json_response:
					users.append(UserGroup(**user))
				users=UserResponse(users=users)
				return users
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def get_members_by_group(groupId:int)-> UserResponse:
		try:
				response = requests.get(f"{GROUP_MS_URL}/groups/get_members/{groupId}/")
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response=json.loads(json_response)
				users = []
				for user in json_response:
					users.append(UserGroup(**user))
				users=UserResponse(users=users)
				return users
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def	get_admins_by_group(groupId:int)-> UserResponse:
		try:
				response = requests.get(f"{GROUP_MS_URL}/groups/get_admins/{groupId}/")
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response=json.loads(json_response)
				users = []
				for user in json_response:
					users.append(UserGroup(**user))
				users=UserResponse(users=users)
				return users
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def get_group(groupId:int) -> GrouppClass:
		try:
				response = requests.get(f"{GROUP_MS_URL}/groups/get_group_by_id/{groupId}/")
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response = json.loads(json_response)
				json_response = GrouppClass(**json_response)
				return json_response
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def create_group(name: str,photo: str,description: str,is_private: bool,owner_id: int,in_requests: typing.List[int],members: typing.List[int],admins: typing.List[int]) -> GrouppClass:
		try:
				response = requests.post(f"{GROUP_MS_URL}/groups/postGroup/",json={"name":name,"photo":photo,"description":description,"is_private":is_private,"owner_id":owner_id,"in_requests":in_requests,"members":members,"admins":admins})
				print("RESPONSE :", response.status_code)
				if response.status_code != 201:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response = json.loads(json_response)
				json_response = GrouppClass(**json_response)
				return json_response
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def edit_group(groupId:int,name: str,photo: str,description: str,is_private: bool,owner_id: int) -> GrouppClass:
		try:
				response = requests.put(f"{GROUP_MS_URL}/groups/putGroup/{groupId}/",json={"name":name,"photo":photo,"description":description,"is_private":is_private,"owner_id":owner_id})
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response = json.loads(json_response)
				json_response = GrouppClass(**json_response)
				return json_response
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def delete_group(groupId:int) -> str:
		try:
				response = requests.delete(f"{GROUP_MS_URL}/groups/deleteGroup/{groupId}/")
				if response.status_code != 204:
					raise GraphQLError(str(response.text))
				text=response.json()
				return text["message"]

		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def add_in_request(userId:int, groupId:int)-> GrouppClass:
	try:
				response = requests.post(f"{GROUP_MS_URL}/groups/add_in_request/{groupId}",json={"in_request":userId})
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response = json.loads(json_response)
				json_response = GrouppClass(**json_response)
				return json_response
	except ValueError as error: # Bad format
			raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
			raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
			raise GraphQLError(f"Error al procesar la respuesta: {error}")
def delete_in_request(userId:int, groupId:int)-> GrouppClass:
	try:
				response = requests.delete(f"{GROUP_MS_URL}/groups/delete_in_request/{groupId}/{userId}")
				print("RESPONSE :", response.status_code)
				print(response.text)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response = json.loads(json_response)	
				json_response = GrouppClass(**json_response)
				return json_response
	except ValueError as error: # Bad format
			raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
			raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
			raise GraphQLError(f"Error al procesar la respuesta: {error}")
def add_user_to_group(userId:int, groupId:int)-> GrouppClass:
	try:
				response = requests.post(f"{GROUP_MS_URL}/groups/add_member/{groupId}",json={"member":userId})
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response = json.loads(json_response)
				json_response = GrouppClass(**json_response)
				return json_response
	except ValueError as error: # Bad format
			raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
			raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
			raise GraphQLError(f"Error al procesar la respuesta: {error}")
def delete_user_from_group(userId:int, groupId:int)-> GrouppClass:
	try:
				response = requests.delete(f"{GROUP_MS_URL}/groups/delete_member/{groupId}/{userId}")
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response = json.loads(json_response)
				json_response = GrouppClass(**json_response)
				return json_response
	except ValueError as error: # Bad format
			raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
			raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
			raise GraphQLError(f"Error al procesar la respuesta: {error}")
def add_admin_to_group(userId:int, groupId:int)-> GrouppClass:
	try:
				response = requests.post(f"{GROUP_MS_URL}/groups/add_admin/{groupId}",json={"admin":userId})
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response = json.loads(json_response)
				json_response = GrouppClass(**json_response)
				return json_response
	except ValueError as error: # Bad format
			raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
			raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
			raise GraphQLError(f"Error al procesar la respuesta: {error}")
def delete_admin_from_group(userId:int, groupId:int)-> GrouppClass:
	try:
				response = requests.delete(f"{GROUP_MS_URL}/groups/delete_admin/{groupId}/{userId}")
				print("RESPONSE :", response.status_code)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response = json.loads(json_response)
				json_response = GrouppClass(**json_response)
				return json_response
	except ValueError as error: # Bad format
			raise GraphQLError(str(error))
	except requests.RequestException as error:  # net errors
			raise GraphQLError(f"Error al contactar la API REST: {error}")
	except KeyError as error:  # Keys error
			raise GraphQLError(f"Error al procesar la respuesta: {error}")
