import sys
import os
import requests
import json
import time
from classes import *

def update_db():
    fp2 = open("NHL_TEAMS.json")
    teamsJson = json.load(fp2)

    for team in teamsJson["teams"]:

        #city = team["locationName"]
        #name = team["teamName"]
        #id = team["id"]
        teamCode = team["abbreviation"]

        #tempTeam = Team(city, name, id, teamCode)

        print(teamCode)

        req = f"https://api-web.nhle.com/v1/roster/{teamCode}/current"

        resp = requests.get(req)

        print(resp.status_code)
        if(resp.status_code != 200):
            print(f"Response for {req} not OK, terminating with code {resp.status_code}...")
            exit()

        jason = json.loads(resp.text)

        fp = open(f"./db2/{teamCode}_temp.json", "w+")
        json.dump(jason, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=3, separators=None)
        fp.close()
    fp2.close()

def pascal_case(name):
     return name[:1].upper() + name[1:].lower()

def fanPts(player):
    return (3*player["goals"] + 2*player["assists"])

#takes user input of player names and returns an array of the names (in pascal case)
def input_names():
    #print("Enter player names in the form \"lastname,lastname,lastname\":")
    inp = input("Enter player surnames (separated by ',' or ' '): ")
    nameList = inp.replace(" ",",").split(',')
    nameListCopy = []
    print(nameList)

    for name in nameList:
        nameListCopy.append(pascal_case(name))

    print(f"NAME COPY = {nameListCopy}")
    return nameListCopy

def find_players(nameList, idTeam):
    playerInfo = {}
    #temporary for each player to have their ID associated with their team code in case two players on the same team have the same name
    playerIdTeam = {}

    for player in nameList: #for every player to be looked up
        for code in idTeam:   #for every team
            #open and load the corresponding JSON for the current team
            fp2 = open(f"./db2/{code}_temp.json")
            teamJson = json.load(fp2)

            for person in teamJson["forwards"]: #for every forward                
                if(player == person["lastName"]["default"]):  #if the last name of the current player matches the last name of the current desired player
                    print(f"Found {player} on " + code)

                    temp_player_info = {"id"        : person["id"],
                                        "team"      : code,
                                        "firstName" : person["firstName"]["default"],
                                        "lastName"  : person["lastName"]["default"]
                                        }
                    
                    tmp = str(player)
                    for entry in playerInfo:
                        if(playerInfo[entry]["lastName"] == temp_player_info["lastName"]):
                            player = f"{player}*"
                    playerInfo[player] = temp_player_info    #add the current player as a key in the dict with their value as their ID
                    player = tmp
            for person in teamJson["defensemen"]: #for every dman      
                if(player == person["lastName"]["default"]):  #if the last name of the current player matches the last name of the current desired player
                    print(f"Found {player} on " + code)

                    temp_player_info = {"id"        : person["id"],
                                        "team"      : code,
                                        "firstName" : person["firstName"]["default"],
                                        "lastName"  : person["lastName"]["default"]
                                        }
                    
                    tmp = str(player)
                    for entry in playerInfo:
                        if(playerInfo[entry]["lastName"] == temp_player_info["lastName"]):
                            player = f"{player}*"
                    playerInfo[player] = temp_player_info    #add the current player as a key in the dict with their value as their ID
                    player = tmp
            fp2.close()
    return playerInfo

def populate_stats(playerInfo, yearStrings):
    req = "https://api-web.nhle.com/v1/player/8481559/landing"
    
    resp = requests.get(req)
    if(resp.status_code != 200):
        print(f"Response for {req} not OK, terminating with code {resp.status_code}...")
        exit()

    playerStats = json.loads(resp.text)
    print(playerStats["seasonTotals"][18]["points"])
    
    for player in playerInfo:
        temp = playerInfo[player]
        print(temp)
    return

def main():

    fp = open("NHL_TEAMS.json", "r")
    nhlJson = json.load(fp)
    fp.close

    idTeam = {}
    for team in nhlJson["teams"]:
        idTeam[team["abbreviation"]] = team["name"]


    #update_db()
    nameList = input_names()

    playerInfo = find_players(nameList, idTeam)
    populate_stats(playerInfo, "20222023")

main()