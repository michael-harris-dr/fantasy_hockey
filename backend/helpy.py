import requests
import json
import constant
import inspect

myself = lambda: inspect.stack()[1][3]

def load_team_ids(filename):
    '''
    load_team_ids
        reads in NHL team information to associate team abbreviation codes and team names    
    
        Parameters:
            filename (str) 
                - literal string name of file where the team info (name, ID and team code) is stored
                - typically "NHL_TEAMS.json"
        Return:
            idTeam ({str:str})
                - a dict of the form {team code : team name}
                - e.g. {NJD : New Jersey Devils}

    '''
    fp = open(filename, "r")
    nhlJson = json.load(fp)
    fp.close()

    idTeam = {}
    for team in nhlJson["teams"]:
        idTeam[team["abbreviation"]] = team["name"]
    return idTeam

pascal_case = lambda name : name[:1].upper() + name[1:].lower() #makes text pascal case (PascalCaseIsLikeThis)

def pascalify_names(nameList):

    nameListCopy = []

    for name in nameList:
        nameListCopy.append(pascal_case(name))

    return nameListCopy

def new_find_players(nameList, idTeam):
    playerInfo = []

    for player in nameList: #for every player to be looked up
        for code in idTeam:   #for every team in the league
            #open and load the corresponding JSON for the current team
            fp2 = open(f"{constant.ROSTERS_PATH}{code}_temp.json")
            teamJson = json.load(fp2)

            for person in teamJson["forwards"]: #for every forward                
                if(player == person["lastName"]["default"]):  #if the last name of the current player matches the last name of the current desired player
                    print(f"{myself()}: Found {player} on " + code)

                    temp_player_info = {"id"        : person["id"],
                                        "team"      : code,
                                        "firstName" : person["firstName"]["default"],
                                        "lastName"  : person["lastName"]["default"]
                                        }
                    
                    tmp = str(player)
                    for entry in playerInfo:
                        if(entry["lastName"] == temp_player_info["lastName"]):
                            player = f"{player}*"
                    playerInfo.append(temp_player_info)    #add the current player as a key in the dict with their value as their ID
                    player = tmp
            for person in teamJson["defensemen"]: #for every dman      
                if(player == person["lastName"]["default"]):  #if the last name of the current player matches the last name of the current desired player
                    print(f"{myself()}: Found {player} on " + code)

                    temp_player_info = {"id"        : person["id"],
                                        "team"      : code,
                                        "firstName" : person["firstName"]["default"],
                                        "lastName"  : person["lastName"]["default"]
                                        }
                    
                    tmp = str(player)
                    for entry in playerInfo:
                        if(entry["lastName"] == temp_player_info["lastName"]):
                            player = f"{player}*"
                    playerInfo.append(temp_player_info)    #add the current player as a key in the dict with their value as their ID
                    player = tmp
            fp2.close()
    print("ERHAFNVUADJIO:")
    print(f"pi: {playerInfo}")
    return playerInfo

def find_players(nameList, idTeam):
    '''
    find_players
        searches every NHL roster to find matches for all given player and associate the player with the team they're on
    
        Parameters:
            nameList ([str])
                - array of player names to be searched for
            idTeam ({str:str})
                - team abbreviation codes associated w/ team names, used as a master list of all NHL teams to search
        Return:
            idTeam ({str:dict})
                - a dict where the key is the player's last name and the value is a dict containing the player's id, team, first name and last name

    '''
    playerInfo = {}

    for player in nameList: #for every player to be looked up
        for code in idTeam:   #for every team in the league
            #open and load the corresponding JSON for the current team
            fp2 = open(f"{constant.ROSTERS_PATH}{code}_temp.json")
            teamJson = json.load(fp2)

            for person in teamJson["forwards"]: #for every forward                
                if(player == person["lastName"]["default"]):  #if the last name of the current player matches the last name of the current desired player
                    print(f"{myself()}: Found {player} on " + code)

                    temp_player_info = {"id"        : person["id"],
                                        "team"      : code,
                                        "firstName" : person["firstName"]["default"],
                                        "lastName"  : person["lastName"]["default"]
                                        }
                    
                    tmp = str(player)
                    for entry in playerInfo:
                        if(entry["lastName"] == temp_player_info["lastName"]):
                            player = f"{player}*"
                    playerInfo[player] = temp_player_info    #add the current player as a key in the dict with their value as their ID
                    player = tmp
            for person in teamJson["defensemen"]: #for every dman      
                if(player == person["lastName"]["default"]):  #if the last name of the current player matches the last name of the current desired player
                    print(f"{myself()}: Found {player} on " + code)

                    temp_player_info = {"id"        : person["id"],
                                        "team"      : code,
                                        "firstName" : person["firstName"]["default"],
                                        "lastName"  : person["lastName"]["default"]
                                        }
                    
                    tmp = str(player)
                    for entry in playerInfo:
                        if(entry["lastName"] == temp_player_info["lastName"]):
                            player = f"{player}*"
                    playerInfo[player] = temp_player_info    #add the current player as a key in the dict with their value as their ID
                    player = tmp
            fp2.close()
    print("ERHAFNVUADJIO:")
    print(f"pi: {playerInfo}")
    return playerInfo

#populates the player's relevant stats (lifetime NHL)
def populate_stats(playerInfo):
    print(f"PI={playerInfo}")
    
    for player in playerInfo:
        print(f"PLAYER={player}")
        req = f"https://api-web.nhle.com/v1/player/{player['id']}/landing"
        resp = requests.get(req)

        playerStats = json.loads(resp.text)

        nhlSeasons = {}
        for season in playerStats["seasonTotals"]:
            if(season["leagueAbbrev"] == "NHL" and season["gameTypeId"] == 2):
                nhlSeasons[season["season"]] = {
                                                    "gp" : season["gamesPlayed"],
                                                    "goals" : season["goals"],
                                                    "assists" : season["assists"],
                                                    "points" : season["points"],
                                                    "shp" : season["shootingPctg"]
                                                }
        player["seasons"] = nhlSeasons
        player["headshot"] = playerStats["headshot"]
    return playerInfo

def separate_namesakes(playerStats):
    for player in playerStats:
        identifier_depth = 0    #uniqueness identifier: 0 for unique player, 1 for same name different team, 2 for same name same team, 3 for same first letter of first name
        i = 0
        for player2 in playerStats:
            if player2 == player:   #ignore checking against own entry
                continue
            elif(player2["lastName"] == player["lastName"]): #if players not the same but same last name
                identifier_depth = max(1, identifier_depth)
                if(player2["team"] == player["team"]): #if players are also on the same team
                    identifier_depth = max(2, identifier_depth)
                    if(player2["firstName"][:1] == player["firstName"][:1]): #if players on the same team share the same first initial
                        identifier_depth = max(3, identifier_depth)
        if(identifier_depth == 0):
            player["special"] = ""
        elif(identifier_depth == 1):
            player["special"] = "(" + player["team"] + ")"
        elif(identifier_depth == 2):
            player["special"] = player["firstName"][:1] + "."
        elif(identifier_depth == 3):
            player["special"] = player["firstName"]
        else:
            player["special"] = "ERROR"
            quit()

def print_player_stats(playerStats):
    for player in playerStats:
        print(playerStats[player]["lastName"] + " " + playerStats[player]["special"] + ":")
        print(playerStats[player]["seasons"])
        for year in playerStats[player]["seasons"]:
            for stat in playerStats[player]["seasons"][year]:
                print(f"\t{stat} : {playerStats[player]['seasons'][year][stat]}")
    return

def get_last_x_seasons(qty, playerInfo):
    newSeasons = {}
    for season in playerInfo["seasons"]:
        if(year_diff(constant.CURRENT_SEASON, season) < qty): #if in most recent x seasons
            newSeasons[season] = dict(playerInfo["seasons"][season])
    print(f"{myself()}: {newSeasons}")

    newPlayer = dict(playerInfo)
    newPlayer["recentSeasons"] = dict(newSeasons)

    #return newPlayer
    #TEMPORARILY DISABLED
    return playerInfo

#TODO: add a weighted consolidated_seasons

year_diff = lambda current, given : int(str(current)[:4]) - int(str(given)[:4])

def find_one_player(name, idTeam):
    found = 0
    for code in idTeam:   #for every team in the league
        #open and load the corresponding JSON for the current team
        fp2 = open(f"{constant.ROSTERS_PATH}{code}_temp.json")
        teamJson = json.load(fp2)

        for person in teamJson["forwards"]: #for every forward                
            if(name == person["lastName"]["default"]):  #if the last name of the current player matches the last name of the current desired player
                print(f"{myself()}: Found {name} on " + code)
                found = 1
        for person in teamJson["defensemen"]: #for every dman      
            if(name == person["lastName"]["default"]):  #if the last name of the current player matches the last name of the current desired player
                print(f"{myself()}: Found {name} on " + code)
                found = 1
        if(found):
            return True
        fp2.close()
    return False
