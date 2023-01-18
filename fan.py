import sys
import os
from time import sleep
from time import strftime, gmtime
import requests
import json
from datetime import date

keyStr = "33667pxcyxpqsjsx7d65bf22"

apiStr = "http://api.sportradar.us/nhl/trial/v7/en/seasons/2015/REG/leaders/offense.json?api_key=" + keyStr

response = requests.get(apiStr)
print(response.text)
print(response.status_code)

json_load = (json.loads(response.text))

gamesJson = json_load['games']

print(gamesJson)