from fastapi import FastAPI
import json
from fastapi.middleware.cors import CORSMiddleware
from fan import *
from typing import Union

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


items = []


@app.get("/health")
def health():
    return {"status" : "up and running"}

@app.get("/items")
def get_items():
    return json.dumps(items)

@app.post("/")
def add_item(request: dict):
    items.append(request["item"]) # Adding item to our todo_items list
    return {"status": "ok", "message": "Item added"} #Sending the API Response back

@app.get("/validatePlayer")
def get_player(Player: str):

    found = valid_player(Player)
    return json.dumps(found)

@app.get("/players")
def get_players(Players: Union[str, None] = None):
    playerStats = get_player_stats(json.loads(Players))
    
    return json.dumps(playerStats)