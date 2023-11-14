import sys
import os
import requests
import json
import time

def update_team_list():
    print("Updating team list...")
    apiStr2 = "https://statsapi.web.nhl.com/api/v1/teams"
    response = requests.get(apiStr2)
    print(f"Updating team list, respone: {response.status_code}")

    if(response.status_code != 200):
        print("Response not OK, terminating...")
    else:
        print("Response 200")
        nhlJson = json.loads(response.text)
    #print(nhlJson)

    fp = open("NHL_TEAMS.json", "w")
    json.dump(nhlJson, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=3, separators=None)
    fp.close()
    print("Teams list finished update.")
    time.sleep(3)
    os.system("clear")

# PARAMS: teamID ()
# OUTPUT: 
# retrieves list of players using a given team ID
def update_player_list(teamID):
    apiStr = f"https://statsapi.web.nhl.com/api/v1/teams/{teamID}/roster" #?expand=team.roster"
    response = requests.get(apiStr)
    print(f"Updating player list for team id={teamID}, response: {response.status_code}")
    if(response.status_code != 200):
        print(f"Response for {apiStr} not OK, terminating...")
    else:
        teamJson = json.loads(response.text)

        teamJson["copyright"] = teamID #changes copyright text to team ID
        #print(nhlJson)
    
        fp = open(f"db/TEAM_ROSTER_{teamID}.json", "w")
        json.dump(teamJson, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=3, separators=None)

        fp.close()

#loops through every team ID and calls the update player list f'n on each
def update_entire_player_list(idList):
    for id in idList:
        update_player_list(id)
    print("All rosters updated...")

#converts a players name to pascal case (e.g. "Smith")
def pascal_case(name):
     return name[:1].upper() + name[1:].lower()

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

def menu_loop(idTeam):
    inp = "0"
    while(inp != "1" and inp != "2"):
        inp = input("(1) Refresh team list and rosters\n(2) Skip\nEnter command: ")
    if(inp == "1"):
        update_team_list()
        update_entire_player_list(idTeam)
        print("\n\n\n")
        return
    elif(inp == "2"):
        return
    else:
        print("critical error 1")
    
def fanPts(player):
    return (3*player["goals"] + 2*player["assists"])

def find_players(nameList, idTeam):
    #find players in the league and store their IDs
    playerIDs = {}

    for player in nameList: #for every player the user requested
        for id in idTeam:   #for every id in the team id list (for each NHL team)
            tmp = player
            #open and load the corresponding JSON for the current team
            fp2 = open(f"./db/TEAM_ROSTER_{id}.json")
            teamJson = json.load(fp2)

            for name in teamJson["roster"]: #for every player on the team
                surname = name["person"]["fullName"].split(" ")[1]  #isolate their last name
                
                if(player == surname):  #if the last name of the current player matches the last name of the current desired player
                    print(f"Found {player} matches {surname} on team: " + idTeam[teamJson["copyright"]])
                    
                    #accounting for repeated names (e.g. "Tkachuk")
                    while player in playerIDs:
                        player = f"{player}*"
                        #print(playerIDs)
                    playerIDs[player] = name["person"]["id"]    #add the current player as a key in the dict with their value as their ID
                player = tmp
            fp2.close()
    return playerIDs

#takes playerIDs to look for and yearStrings to indicate time period
#outputs a dict w/ key=player_name and value=dict of games played, goals, assists, sh%, shots
def populate_stats(playerIDs, yearStrings):
    playerStats = {}

    trackedStats = ["goals", "assists", "shots", "games"] #volume stats, shot% needs to be done separately
    playerStats = {}
    for years in yearStrings:
        for player in playerIDs:

            if not player in playerStats:
                playerStats[player] = {}

            apiStr = f"https://statsapi.web.nhl.com/api/v1/people/{playerIDs[player]}/stats?stats=statsSingleSeason&season={years}"
            response = requests.get(apiStr)
            playerJson = json.loads(response.text)
            
            if (response.status_code != 200):
                print(response.status_code)

            if "shutouts" in playerJson["stats"][0]["splits"][0]["stat"]:
                print(f"{player} is goalie")
            else:
                stats = playerJson["stats"][0]["splits"][0]["stat"]
            
            for stat in trackedStats:
                if stat in playerStats[player]:
                    playerStats[player][stat] += stats[stat]
                else:
                    playerStats[player][stat] = stats[stat]
    return playerStats

#TODO: add players previous years stats and adjust xFP (expected fantasy points) accordingly
#TODO: add GP as stat and factor into xFP

def calculate_stats(playerList):
    for player in playerList:
        playerList[player]["sh%"] = round(100 * playerList[player]["goals"] / playerList[player]["shots"], 1)

    return playerList

def expected_fan_pts(player):
    #TODO: create xFP based on a given shooting percentage and extrapolating gp to the highest of any team this season
    return 0

def get_most_gp():
    apiStr = "https://statsapi.web.nhl.com/api/v1/standings"
    response = requests.get(apiStr)
    if(response.status_code != 200):
        print(f"Response for {apiStr} not OK, terminating...")
    else:
        standingsJson = json.loads(response.text)

        high = 0
        
        for team in standingsJson["records"][0]["teamRecords"]:
            if team["gamesPlayed"] > high:
                high = team["gamesPlayed"]

    return high

def proj_stats_to_current():
    return
    #TODO: make a stat and project it to max GP based on highest gp by one team (get_most_gp())


def print_player_stats_all(currentYearStatsList):
        for player in currentYearStatsList:
            print(f"{player : ^12} = gp: " + str(currentYearStatsList[player]["games"])
            + "\tg: " + str(currentYearStatsList[player]["goals"])
            + "\ta: " + str(currentYearStatsList[player]["assists"])
            + "\tFP: " + str(fanPts(currentYearStatsList[player])))

#MAIN()###########################################################################################################

def main():

    #idTeam is a dict with key = team ID and value = associated team's name
    #e.g. idTeam["1"] = "New Jersey Devils"
    idTeam = {}

    fp = open("NHL_TEAMS.json", "r")
    nhlJson = json.load(fp)

    #populate idTeam for each team/ID pair
    for team in nhlJson["teams"]:
        idTeam[team["id"]] = team["name"]

    menu_loop(idTeam)

    #nameList is an array of the last names of players
    #e.g. ["McDavid", "Matthews", "Mackinnon"]
    nameList = input_names()

    #playerIDs is a dict with key = player name and value = player's identification number
    #e.g. Matthews -> 8479318
    playerIDs = find_players(nameList, idTeam)
    print(playerIDs)

    currentYearStatsList = populate_stats(playerIDs, ["20222023"])
    currentYearStatsList = calculate_stats(currentYearStatsList)
    print(currentYearStatsList)

#    twoYearStats = populate_stats(playerIDs, ["20222023", "20212022"])
#    twoYearStats = calculate_stats(twoYearStats)
#    print(f"_{twoYearStats}")

#    threeYearStats = populate_stats(playerIDs, ["20222023", "20212022", "20202021"])
#    threeYearStats = calculate_stats(threeYearStats)
#    print(f"__{threeYearStats}")

    #isolating useful stats

    
    print_player_stats_all(currentYearStatsList)

#    calculate_stats(twoYearStats)
    get_most_gp()
    fp.close()

main()
#FIN