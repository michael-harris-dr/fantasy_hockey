from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status
import json
import os
from helpy import myself

API_KEY_HEADER = APIKeyHeader(name="X-API-key")

def validate_api_key(x_api_key: str = Security(API_KEY_HEADER)):
	keyList = ["temp120681689", "4132"]
	if x_api_key in keyList:
		print(f"{myself()}:\tValidated API Key".expandtabs(20))
		return x_api_key
	raise HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="API key invalid :/"
	)
