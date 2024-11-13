import csv
import os
from utils.api_calls import get_fantasy_point_projections, get_nfl_player_info

# CSV file path
CSV_FILE_WR = 'nfl_fantasy_projections_wr.csv'
CSV_FILE_TE = 'nfl_fantasy_projections_te.csv'
CSV_FILE_RB = 'nfl_fantasy_projections_rb.csv'
CSV_FILE_QB = 'nfl_fantasy_projections_qb.csv'
CSV_FILE_PK = 'nfl_fantasy_projections_pk.csv'

# Create the CSV file and define its columns
def create_csv(file_path, pos):
    # Define the column headers (adjust as per the API response structure)
    headers = []
    if pos == 'WR':
        headers = ['Player Name', 'Projected Season Rush Yards', 'Projected Season Rush TDs',
                   'Projected Season Receptions', 'Projected Season Yards', 'Projected Season TDs',
                   'Season Reception Average', 'Season TDs Average', 'Season Yards Average', 'Injury Status']

    elif pos == 'RB':
        headers = ['Player Name', 'Projected Season Rush Yards', 'Projected Season Rush TDs',
                   'Projected Season Receptions', 'Projected Season Yards', 'Projected Season TDs']

    elif pos == 'QB':
        headers = ['Player Name', 'Projected Season Rushing Yards', 'Projected Season Rushing TDs',
                   'Projected Season Passing TDs', 'Projected Season Passing Yards', 'Projected Season INTs']

    elif pos == 'TE':
        headers = ['Player Name', 'Projected Season Rush Yards', 'Projected Season Rush TDs',
                   'Projected Season Receptions', 'Projected Season Yards', 'Projected Season TDs']

    elif pos == 'PK':
        headers = ['Player Name', 'Projected Season Made FGs', 'Projected Season Missed FGs',
                   'Projected Season Made XPs', 'Projected Season Missed XPs']

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        print(f"CSV file '{file_path}' created with headers: {headers}")


# Add a single row of data to the CSV from the API response
def add_data_to_csv(file_path, pos):
    # Fetch data from the API
    data = get_fantasy_point_projections(week='season')
    if data and 'body' in data:
        projections = data['body'].get('playerProjections', [])
        for player in projections:
            if pos == 'WR' and projections[player].get('pos') == 'WR':
                player_name = projections[player].get('longName')
                season_rush_prediction = projections[player]['Rushing'].get('rushYds')
                season_rush_td_prediction = projections[player]['Rushing'].get('rushTD')
                season_rec_prediction = projections[player]['Receiving'].get('receptions')
                season_yard_prediction = projections[player]['Receiving'].get('recYds')
                season_red_td_prediction = projections[player]['Receiving'].get('recTD')
                player_info_raw = get_nfl_player_info(player_name)
                player_info = player_info_raw["body"][0]
                games_played = player_info["stats"].get("gamesPlayed")
                if "Receiving" in player_info["stats"]:
                    average_season_rec = float(player_info["stats"]['Receiving'].get('receptions')) / int(games_played)
                    average_season_rec_td = float(player_info["stats"]['Receiving'].get('recTD')) / int(games_played)
                    average_season_yards = float(player_info["stats"]['Receiving'].get('recYds')) / int(games_played)
                else:
                    print(player_name)
                    average_season_rec = 0
                    average_season_rec_td = 0
                    average_season_yards = 0
                injury_info = player_info['injury']
                injury_status = 0
                if injury_info.get('designation') != '':
                    if injury_info.get('designation') == 'Questionable':
                        injury_status = 1
                    elif injury_info.get('designation') == 'Doubtful':
                        injury_status = 2
                    elif injury_info.get('designation') == 'Out':
                        injury_status = 3
                    elif injury_info.get('designation') == 'Injured Reserve':
                        injury_status = 4
                with open(file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([player_name, season_rush_prediction, season_rush_td_prediction,
                                     season_rec_prediction, season_yard_prediction, season_red_td_prediction,
                                     average_season_rec, average_season_rec_td, average_season_yards, injury_status])

            elif pos == 'RB' and (projections[player].get('pos') == 'RB' or projections[player].get('pos') == 'FB'):
                player_name = projections[player].get('longName')
                season_rush_prediction = projections[player]['Rushing'].get('rushYds')
                season_rush_td_prediction = projections[player]['Rushing'].get('rushTD')
                season_rec_prediction = projections[player]['Receiving'].get('receptions')
                season_yard_prediction = projections[player]['Receiving'].get('recYds')
                season_red_td_prediction = projections[player]['Receiving'].get('recTD')
                with open(file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([player_name, season_rush_prediction, season_rush_td_prediction,
                                     season_rec_prediction, season_yard_prediction, season_red_td_prediction])

            elif pos == 'TE' and projections[player].get('pos') == 'TE':
                player_name = projections[player].get('longName')
                season_rush_prediction = projections[player]['Rushing'].get('rushYds')
                season_rush_td_prediction = projections[player]['Rushing'].get('rushTD')
                season_rec_prediction = projections[player]['Receiving'].get('receptions')
                season_yard_prediction = projections[player]['Receiving'].get('recYds')
                season_red_td_prediction = projections[player]['Receiving'].get('recTD')
                with open(file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([player_name, season_rush_prediction, season_rush_td_prediction,
                                     season_rec_prediction, season_yard_prediction, season_red_td_prediction])
            elif pos == 'PK' and projections[player].get('pos') == 'PK':
                print(projections[player])
                player_name = projections[player].get('longName')
                season_fg_made_prediction = projections[player]['Kicking'].get('fgMade')
                season_fg_missed_prediction = projections[player]['Kicking'].get('fgMissed')
                season_xp_made_prediction = projections[player]['Kicking'].get('xpMade')
                season_xp_missed_prediction = projections[player]['Kicking'].get('xpMissed')
                with open(file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([player_name, season_fg_made_prediction, season_fg_missed_prediction,
                                     season_xp_made_prediction, season_xp_missed_prediction])
            elif pos == 'QB' and projections[player].get('pos') == 'QB':
                player_name = projections[player].get('longName')
                season_rush_prediction = projections[player]['Rushing'].get('rushYds')
                season_rush_td_prediction = projections[player]['Rushing'].get('rushTD')
                season_pass_td_prediction = projections[player]['Passing'].get('passTD')
                season_pass_yards_prediction = projections[player]['Passing'].get('passYds')
                season_int_prediction = projections[player]['Passing'].get('int')
                with open(file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([player_name, season_rush_prediction, season_rush_td_prediction,
                                     season_pass_td_prediction, season_pass_yards_prediction, season_int_prediction])
    return None




