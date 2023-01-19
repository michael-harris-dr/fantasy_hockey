import sys
import os
from time import sleep
from time import strftime, gmtime
import requests
import json
from datetime import date


class Player:
    def __init__(self, name, goals, assists, shooting_percentage):
        self.name = name
        self.goals = goals
        self.assists = assists
        self.shooting_percentage = shooting_percentage

keyStr = "33667pxcyxpqsjsx7d65bf22"

apiStr = "http://api.sportradar.us/nhl/trial/v7/en/seasons/2022/REG/leaders/offense.json?api_key=" + keyStr
##########################################################/YEAR^/ refers to the start year of the season ("2022" is 2022-2023 season)

response = requests.get(apiStr)
#print(response.text)
print("Response status code: " + str(response.status_code))

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

apiStr2 = "https://statsapi.web.nhl.com/api/v1/people/8478483/stats?stats=statsSingleSeason&season=20222023"
response = requests.get(apiStr2)
print(response.text)

for i in range(5):
    print(statsJson["categories"][1]["ranks"][i]["player"]["full_name"] + " " + str(statsJson["categories"][1]["ranks"][i]["statistics"]["total"]["goals"]))