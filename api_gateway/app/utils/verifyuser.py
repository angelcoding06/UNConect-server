import requests
from app.auth_ms.auth.definitions.auth import AuthClass, TokenClass, Role
from strawberry.exceptions import GraphQLError
from app.auth_ms.const import AUTH_MS_URL
from typing import Optional
import json

URL = f"{AUTH_MS_URL}/auth"
def jsonToAuthClass(json) -> AuthClass:
    auth = AuthClass(**json)
    auth.role = Role(auth.role)
    return auth

def verifyUser(token:str):
	try:
		response = requests.post(f"{URL}/validate?token={token}")
		print("Response desde verify :",response)
		print("Status: ", response.status_code)
		print("Text: ", response.text)
		if response.status_code == 404:
				return "UNAUTHORIZED"
		auth = response.json()
		return jsonToAuthClass(auth)
	except:
		return "UNAUTHORIZED"
