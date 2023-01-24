import requests

SEASON_SCHEDULE_TEMPLATE = "https://statsapi.web.nhl.com/api/v1/schedule?startDate={0}-08-01&endDate={1}-07-31&hydrate=team,linescore,broadcasts(all),tickets,game(content(media(epg)),seriesSummary),radioBroadcasts,metadata,seriesSummary(series)&site=en_nhl&teamId=&gameType=R&timecode="

GAME_DETAILS_TEMPLATE = "https://statsapi.web.nhl.com/api/v1/game/{0}/feed/live?site=en_nhl"

NHL_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"}

TEAM_FRANCHISE_MAPPINGS = {
    1: 23,
    2: 22,
    3: 10,
    4: 16,
    5: 17,
    6: 6,
    7: 19,
    8: 1,
    9: 30,
    10: 5,
    11: 35,
    12: 26,
    13: 33,
    14: 31,
    15: 24,
    16: 11,
    17: 12,
    18: 34,
    19: 18,
    20: 21,
    21: 27,
    22: 25,
    23: 20,
    24: 32,
    25: 15,
    26: 14,
    27: 28,
    28: 29,
    29: 36,
    30: 37,
    31: 15,
    32: 27,
    33: 28,
    34: 26,
    35: 23,
    36: 3,
    37: 4,
    38: 9,
    39: 9,
    40: 12,
    41: 2,
    42: 4,
    43: 7,
    44: 8,
    45: 3,
    46: 13,
    47: 21,
    48: 23,
    49: 13,
    50: 12,
    51: 8,
    52: 35,
    53: 28,
    54: 38,
    55: 39,
    56: 13,
    57: 5,
    58: 5
}

if __name__ == '__main__':
    tandem_shutouts = dict()
    for season_start in range(1967, 2023):
        print(f"Processing season: {season_start}-{season_start + 1}")

        # Get the season schedule and find all games with a shutout.
        schedule_request = SEASON_SCHEDULE_TEMPLATE.format(season_start, season_start + 1)
        schedule_response = requests.get(url=schedule_request, headers=NHL_HEADERS)
        schedule_json = schedule_response.json()

        # We get back a list of dates, iterate through each.
        for date in schedule_json["dates"]:
            for game in date["games"]:
                if game["status"]["statusCode"] != "7":
                    # We only want games marked as finished.
                    continue
                for team_pair in [("away", "home"), ("home", "away")]:
                    if game["teams"][team_pair[0]]["score"] == 0:
                        game_id = game["gamePk"]
                        game_request = GAME_DETAILS_TEMPLATE.format(game_id)
                        game_response = requests.get(game_request, headers=NHL_HEADERS)
                        game_json = game_response.json()
                        team_goalies = game_json["liveData"]["boxscore"]["teams"][team_pair[1]]["goalies"]
                        if len(team_goalies) > 1:
                            tandem = tuple(sorted(team_goalies))
                            if tandem not in tandem_shutouts:
                                tandem_shutouts[tandem] = []
                            tandem_shutouts[tandem].append(game_id)

    with open(r"C:\Temp\tandem_so_old.txt", "a") as out_file:
        for k, v in tandem_shutouts.items():
            out_file.write(f"{k}|{v}\n")