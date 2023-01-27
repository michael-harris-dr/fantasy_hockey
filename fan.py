import sys
import os
from time import sleep
from time import strftime, gmtime
import requests
import json


def argCount():
    return len(sys.argv) - 1

keyStr = "33667pxcyxpqsjsx7d65bf22"

apiStr = "http://api.sportradar.us/nhl/trial/v7/en/seasons/2022/REG/leaders/offense.json?api_key=" + keyStr
##########################################################/YEAR^/ refers to the start year of the season ("2022" is 2022-2023 season)

response = requests.get(apiStr)

print("Response status code: " + str(response.status_code))

#
#
# Get nhl stat leaders and dump to external file
#
#
if(response.status_code != 200):
    print("Response not OK, terminating...")
    statsJson = json.loads("{}")
    fp = open("json_dump.json", "w")
    json.dump(statsJson, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=3, separators=None)
else:
    statsJson = (json.loads(response.text))

    #print(statsJson)

    fp = open("json_dump.json", "w")
    json.dump(statsJson, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=3, separators=None)

    #0	games_played
    #1	goals
    #2	assists
    #3	shots
    #4	points
    #5	faceoffs_won
    #6+	even str./shorthanded/per-game stats

    print(statsJson["categories"][1]["ranks"][0]["rank"])

apiStr2 = "https://statsapi.web.nhl.com/api/v1/teams"
response = requests.get(apiStr2)
print(response.status_code)

#
#
# Get list of NHL teams and add their ID/name in a dict
#
#
if(response.status_code != 200):
    print("Response not OK, terminating...")
else:
    nhlJson = json.loads(response.text)
    #print(nhlJson)

    fp = open("nhl_json_dump.json", "w")
    json.dump(nhlJson, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=3, separators=None)

    idTeam = {}#dict()

    for team in nhlJson["teams"]: #for each team
        idTeam[team["id"]] = team["name"] #add the team name to the dict w/ the team ID as the key

    print(idTeam)


#
#
# Find list of players on each team
#
#
apiStr = "https://statsapi.web.nhl.com/api/v1/teams/1/roster" #?expand=team.roster"
response = requests.get(apiStr)
print(response.status_code)
if(response.status_code != 200):
    print(f"Response for {apiStr} not OK, terminating...")
else:
    teamJson = json.loads(response.text)
    #print(nhlJson)

    fp = open("team_json_dump.json", "w")
    json.dump(teamJson, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=3, separators=None)


for team in nhlJson["teams"]:
    apiStr = f"https://statsapi.web.nhl.com/api/v1/teams/{team['id']}/roster" #?expand=team.roster"
    response = requests.get(apiStr)
    p = json.loads(response.text)
    print(p["roster"][1]["person"]["fullName"])




