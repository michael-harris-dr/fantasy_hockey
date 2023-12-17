from fastapi import FastAPI, Security
import json
from fastapi.middleware.cors import CORSMiddleware
from fan import *
from typing import Union
import os
from security import *
from helpy import myself

app = FastAPI()

origins = ["*"]
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
	expose_headers=["*"]
)

@app.get("/health", status_code=200)
def health():
	return {"status" : "up and running"}

@app.get("/validatePlayer", dependencies=[Security(validate_api_key)])
def get_player(Player: str):
	found = valid_player(Player)
	return json.dumps(found)

@app.get("/players", dependencies=[Security(validate_api_key)])
def get_players(Players: Union[str, None] = None):
	passed = json.loads(Players)
	print(passed)
	playerStats = get_player_stats(passed)
	
	return json.dumps(playerStats)

