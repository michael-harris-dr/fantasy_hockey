import sys
import os
from time import sleep
from time import strftime, gmtime
import requests
import json
from datetime import date

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
    i = 0
    id = 0
    while(i != -1): #emulating a do-while to find Vegas at the end of the file
        currId = nhlJson["teams"][i]["id"]
        currTeam = nhlJson["teams"][i]["name"]
    
        #print(nhlJson["teams"][i]["id"])
        #print(nhlJson["teams"][i]["name"])
        if(currId > 0): #team exists at the current ID
            idTeam[currId] = currTeam
        if(currId == 55):
            print("Found Seattle")
            i = -1
        else:
            i += 1

    print(idTeam)

