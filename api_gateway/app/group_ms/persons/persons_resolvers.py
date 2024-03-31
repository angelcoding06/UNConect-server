import requests
from app.group_ms.persons.definitions.persons import PersonGroupResponse, PersonGroupClass
from strawberry.exceptions import GraphQLError
from app.const import GROUP_MS_URL
import typing
import json

def get_person_group()-> PersonGroupResponse:
		try:
				response = requests.get(f"{GROUP_MS_URL}/groups/getPerson/")
				print(response.content)
				if response.status_code != 200:
						raise GraphQLError(str(response.text))
				json_response = response.text
				json_response=json.loads(json_response)
				users = []
				for person in json_response:
					users.append(PersonGroupClass(**person))
				users=PersonGroupResponse(persons=users)
				return users
		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def create_person_group(user_id:str) -> PersonGroupClass:
		try:
				response = requests.post(f"GROUP_MS_URL/groups/postPerson/", json = {"user_id":user_id})
				text=response.text
				text=json.loads(text)
				if response.status_code == 404:
						raise GraphQLError(str(response.text))
				return PersonGroupClass(**text)

		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def edit_person_group(user_id:str,id:int):
		try:
				response = requests.put(f"GROUP_MS_URL/groups/putPerson/{id}/", json = {"user_id":user_id})
				if response.status_code != 200:
						raise GraphQLError((response.text))
				text=response.text
				text=json.loads(text)
				return PersonGroupClass(**text)

		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")

def delete_person_group(id:int):
		try:
				response = requests.delete(f"GROUP_MS_URL/groups/deletePerson/{id}")
				if response.status_code != 200:
					raise GraphQLError(str(response.text))
				text=response.text
				return text

		except ValueError as error: # Bad format
				raise GraphQLError(str(error))
		except requests.RequestException as error:  # net errors
				raise GraphQLError(f"Error al contactar la API REST: {error}")
		except KeyError as error:  # Keys error
				raise GraphQLError(f"Error al procesar la respuesta: {error}")
