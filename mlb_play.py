import statsapi
import requests
import json
from collections import defaultdict
import numpy as np
import pandas as pd
import pprint

#
# response = requests.get("https://statsapi.mlb.com/api/v1/leagueLeaderTypes")
# json_obj = json.dumps(response.json())
# json_object = json.loads(json_obj)
# json_formatted_str = json.dumps(json_object, indent=2)
#
# print("League Leader Types")
# print(json_formatted_str)
#
# response = requests.get("https://statsapi.mlb.com/api/v1/statTypes")
# json_obj = json.dumps(response.json())
# json_object = json.loads(json_obj)
# json_formatted_str = json.dumps(json_object, indent=2)
#
# print("Stat Types")
# print(json_formatted_str)
#
teams_and_ids = defaultdict(str)
counter = 0
response = requests.get("https://statsapi.mlb.com/api/v1/teams")
for team in response.json()['teams']:
    try:
        if team['sport']['name'] == "Major League Baseball":
            teams_and_ids[team['name']] = team['id']
    except KeyError:
        continue

print(teams_and_ids)
# for row in teams_and_ids.items():
#     print(row)
#
# print("statGroups")
# print(statsapi.meta('statGroups'))
#
# print("standingTypes")
# print(statsapi.meta('standingsTypes'))
#


# def boxscore_data(team_name, schedule_obj):
#
#     season_linescore_dict = defaultdict(list)
#
#     for x in schedule_obj:
#
#         if x['status'] == 'Final':
#
#             season_linescore_dict[x['game_id']].append(x['game_date'])
#             season_linescore_dict[x['game_id']].append(team_name)
#
#             # print("G_ID:", x['game_id'])
#             # print("Date: ", x['game_date'])
#             # print("Main Team", team_name)
#
#             if x['away_name'] == team_name:
#                 # print("Home Name:", x['home_name'])
#                 season_linescore_dict[x['game_id']].append(x['home_name'])
#                 season_linescore_dict[x['game_id']].append("N")
#             else:
#                 # print("Away Name:", x['away_name'])
#                 season_linescore_dict[x['game_id']].append(x['away_name'])
#                 season_linescore_dict[x['game_id']].append("Y")
#
#             # print("Double Header:", x['doubleheader'])
#             # print("----------------------------")
#             season_linescore_dict[x['game_id']].append(x['doubleheader'])
#
#     max_inning = 0
#     for game_id in season_linescore_dict.keys():
#
#         response_obj = requests.get(f"https://statsapi.mlb.com/api/v1/game/{game_id}/linescore")
#         json_obj = json.dumps(response_obj.json())
#         json_object = json.loads(json_obj)
#         for row in json_object['innings']:
#             if row['num'] > max_inning:
#                 max_inning = row['num']
#             try:
#                 if season_linescore_dict[game_id][3] == "Y":
#                     # print(row['home']['runs'])
#                     season_linescore_dict[game_id].append(row['home']['runs'])
#                 else:
#                     season_linescore_dict[game_id].append(row['away']['runs'])
#                     # print(row['away']['runs'])
#             except KeyError:
#                 # print(row)
#                 season_linescore_dict[game_id].append(0)
#
#     # print(season_linescore_dict)
#     # print(max_inning)
#     max_team_inning_played = [str(x) for x in range(1, max_inning+1)]
#     season_linescore = pd.DataFrame.from_dict(season_linescore_dict, columns=["date", "team", "opp", "H", "DBH"] + max_team_inning_played,  orient='index')
#
#     season_linescore.index.name = "game_id"
#     season_linescore = season_linescore.fillna(0)
#     season_linescore.to_csv(f"season_runs_per_inning_{team_name}.csv")
#
# team = "New York Yankees"
#
# schedule = statsapi.schedule(start_date="04/01/2021", end_date="07/04/2021", team=teams_and_ids.get(team))
#
# boxscore_data(team, schedule)
