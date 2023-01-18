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

print(statsJson["categories"][1]["ranks"][0]["rank"])