from helpy import *

def valid_player(name):
    name = pascal_case(name)
    idTeam = load_team_ids(constant.TEAM_LIST_PATH)
    return(find_one_player(name, idTeam))

def get_player_stats(nameList):
    nameList = pascalify_names(nameList)
    idTeam = load_team_ids(constant.TEAM_LIST_PATH)
    playerInfo = find_players(nameList, idTeam)
    playerStats = populate_stats(playerInfo)
    separate_namesakes(playerStats)

    #print_player_stats(playerStats)

    for player in playerStats:
        playerStats[player] = get_last_x_seasons(2, playerStats[player])
    return playerStats

def update_db():
    '''
    update_db()
        updates every team roster JSON by pulling from 'https://api-web.nhle.com/v1/roster/{teamCode}/current'
    '''
    fp2 = open("NHL_TEAMS.json")
    teamsJson = json.load(fp2)

    for team in teamsJson["teams"]:

        teamCode = team["abbreviation"]

        req = f"https://api-web.nhle.com/v1/roster/{teamCode}/current"
        resp = requests.get(req)

        if(resp.status_code != 200):
            print(f"{myself()}: Response for {req} not OK, terminating with code {resp.status_code}...")
            exit()

        jason = json.loads(resp.text)

        fp = open(f"{constant.ROSTERS_PATH}{teamCode}_temp.json", "w+")
        json.dump(jason, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=3, separators=None)
        fp.close()
    fp2.close()