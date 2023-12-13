from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status
import json

API_KEY_HEADER = APIKeyHeader(name="X-API-key")

def validate_api_key(x_api_key: str = Security(API_KEY_HEADER)):
	fp = open("api_keys.json")
	keyList = json.load(fp)
	print(x_api_key)
	print(x_api_key == "temp120681689")

	if x_api_key in keyList:
		print("FOUND")
		return x_api_key
	raise HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="API key invalid :/"
	)
