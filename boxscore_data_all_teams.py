import argparse
import json
import statsapi
import requests
import pandas as pd

from collections import defaultdict
from teams_and_ids import teams_and_ids

parser = argparse.ArgumentParser(description="****Creates a csv file in path given displaying amount of runs for each inning every game inbetween the dates****")

def boxscore_data(team_name, schedule_obj):

    season_linescore_dict = defaultdict(list)

    for x in schedule_obj:
        if x['status'] == 'Final':

            if not season_linescore_dict[x['game_id']]:
                season_linescore_dict[x['game_id']].append(x['game_date'])
                season_linescore_dict[x['game_id']].append(team_name)

                if x['away_name'] == team_name:
                    season_linescore_dict[x['game_id']].append(x['home_name'])
                    season_linescore_dict[x['game_id']].append("N")
                else:
                    season_linescore_dict[x['game_id']].append(x['away_name'])
                    season_linescore_dict[x['game_id']].append("Y")

                season_linescore_dict[x['game_id']].append(x['doubleheader'])
            elif KeyError:
                continue

    max_inning = 0
    for game_id in season_linescore_dict.keys():

        response_obj = requests.get(f"https://statsapi.mlb.com/api/v1/game/{game_id}/linescore")
        json_obj = json.dumps(response_obj.json())
        json_object = json.loads(json_obj)
        for row in json_object['innings']:
            if row['num'] > max_inning:
                max_inning = row['num']
            try:
                if season_linescore_dict[game_id][3] == "Y":
                    season_linescore_dict[game_id].append(row['home']['runs'])
                else:
                    season_linescore_dict[game_id].append(row['away']['runs'])
            except KeyError:
                season_linescore_dict[game_id].append(0)

    max_team_inning_played = [str(x) for x in range(1, max_inning+1)]
    season_linescore = pd.DataFrame.from_dict(season_linescore_dict, columns=["date", "team", "opp", "H", "DBH"] + max_team_inning_played,  orient='index')

    season_linescore.index.name = "game_id"
    season_linescore = season_linescore.fillna(0)

    return season_linescore


parser.add_argument("start_date",
                    help="Put in Quotes. Format \"MM/DD/YYYY\". Beginning date for boxscore")
parser.add_argument("end_date",
                    help="Put in Quotes. Format \"MM/DD/YYYY\". Ending date for boxscore")
parser.add_argument("folder_path",
                    help="Put in Quotes. Format \"Desktop\docuement\example\". Ending date for boxscore")
args = parser.parse_args()

try:

    final_df_lists = []

    for team, team_id in teams_and_ids.items():
        schedule = statsapi.schedule(start_date=args.start_date, end_date=args.end_date, team=team_id)
        temp_df = boxscore_data(team, schedule)
        final_df_lists.append(temp_df)
        print(team)

    final_df = pd.concat(final_df_lists)
    final_df = final_df.fillna(0)
    final_df.to_excel(args.folder_path + f"all_mlb_teams.xlsx")

except:
    print("Error with parameters according to the data service. Please use command 'python boxscore_data_one_team.py -h' for more insight on the parameter and function use.")
