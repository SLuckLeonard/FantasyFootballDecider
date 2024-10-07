from utils.api_calls import (get_fantasy_point_projections, get_nfl_teams, get_nfl_games_for_player,
                             get_nfl_games_for_week, get_nfl_player_headshot)


def compare_players(player_a_id, player_b_id, week, player_a_name, player_b_name):
    """
    Compares two NFL players based on fantasy point projections, team performance, and recent stats.

    :param week: Week for comparison
    :param player_a_name: Player name for first player
    :param player_b_name: Player name for second player
    :param player_a_id: ID of the first player to compare.
    :param player_b_id: ID of the second player to compare.
    :return: A string indicating which player is better for a fantasy start.
    """

    # 1. Get Fantasy Projections
    player_a_projections = get_fantasy_point_projections(player_id=player_a_id)
    player_b_projections = get_fantasy_point_projections(player_id=player_b_id)

    if not player_a_projections or not player_b_projections:
        return "Error: Could not retrieve projections for one or both players."

    player_a_points = get_player_week_points(player_a_id)
    player_b_points = get_player_week_points(player_b_id)

    # 2. Get Team Performance
    teams = get_nfl_teams()
    if not teams:
        return "Error: Could not retrieve team information."

    player_a_team_id = get_player_team(player_a_projections)
    player_b_team_id = get_player_team(player_b_projections)

    # Extract team performance (e.g., win/loss record, standings)
    player_a_team_stats = get_player_team_stats(player_a_team_id, teams)
    # print(player_a_team_stats)
    player_b_team_stats = get_player_team_stats(player_b_team_id, teams)
    # print(player_b_team_stats)

    if not player_a_team_stats or not player_b_team_stats:
        return "Error: Could not retrieve team stats for one or both players."

    player_a_updated_proj = player_a_points * player_a_team_stats
    player_b_updated_proj = player_b_points * player_b_team_stats

    # 3. Get Recent Player Performance
    player_a_recent_games = get_nfl_games_for_player(player_a_id, number_of_games=week-1)
    player_b_recent_games = get_nfl_games_for_player(player_b_id, number_of_games=week-1)

    if not player_a_recent_games or not player_b_recent_games:
        return "Error: Could not retrieve recent game data for one or both players."

    player_a_season_performance = calculate_average_fantasy_points(player_a_recent_games)/(week - 1)
    player_b_season_performance = calculate_average_fantasy_points(player_b_recent_games)/(week - 1)

    # Get just last week
    player_a_lastweek_performance = get_last_week_performance(player_a_recent_games)
    player_b_lastweek_performance = get_last_week_performance(player_b_recent_games)

    # 4. Calculate Final Scores
    player_a_solo_pred_score = (player_a_updated_proj + player_a_season_performance + player_a_lastweek_performance)/3
    player_b_solo_pred_score = (player_b_updated_proj + player_b_season_performance + player_b_lastweek_performance)/3

    # 5. Calculate opponent toughness
    player_a_position = get_player_pos(player_a_projections)
    player_b_position = get_player_pos(player_b_projections)
    player_a_matchup_avg_points_allowed = get_player_matchup_stats(player_a_team_id, week,
                                                                   player_a_position, player_a_recent_games)
    player_b_matchup_avg_points_allowed = get_player_matchup_stats(player_b_team_id, week,
                                                                   player_b_position, player_b_recent_games)

    # 6. Take Final Scores with opponent toughness
    player_a_score = float(((player_a_solo_pred_score * 7) + player_a_matchup_avg_points_allowed)/8)
    player_b_score = float(((player_b_solo_pred_score * 7) + player_b_matchup_avg_points_allowed)/8)

    # 7. Compare and Return the Result
    if player_a_score > player_b_score:
        return (f"Start {player_a_name} with estimated fantasy points of {player_a_score:.2f} "
                f"over {player_b_name} with estimated fantasy points of {player_b_score:.2f}")
    else:
        return (f"Start {player_b_name} with estimated fantasy points of {player_b_score:.2f} "
                f"over {player_a_name} with estimated fantasy points of {player_a_score:.2f}")


def get_player_id(player_name):
    """
    Fetches the player ID for the given player name.
    """
    data = get_fantasy_point_projections(week='season')

    if data and 'body' in data:
        projections = data['body'].get('playerProjections', [])
        for player in projections:
            playername = projections[player].get('longName')
            if playername.lower() == player_name.lower():
                return player
    return None


def get_player_week_points(player_id):
    """
    Fetches the player avg points for the given playerID.
    """
    data = get_fantasy_point_projections(week='season')

    if data and 'body' in data:
        projections = data['body'].get('playerProjections', [])
        for player in projections:
            if player == player_id:
                rush_fantasypoints = (float(projections[player]['Rushing'].get('rushYds'))/10 +
                                      float(projections[player]['Rushing'].get('rushTD'))*6)
                pass_fantasypoints = (float(projections[player]['Passing'].get('passYds'))*.04 +
                                      float(projections[player]['Passing'].get('passTD'))*4 -
                                      float(projections[player]['Passing'].get('int'))*2)
                receiving_fantasypoints = (float(projections[player]['Receiving'].get('recTD'))*6 +
                                           float(projections[player]['Receiving'].get('receptions')) +
                                           float(projections[player]['Receiving'].get('recYds'))*.01)
                fumble_fantasypoints = float(projections[player].get('fumblesLost'))*2
                twopoint_fantasypoints = float(projections[player].get('twoPointConversion')) * 2
                fantasy_points = (rush_fantasypoints + pass_fantasypoints + receiving_fantasypoints -
                                  fumble_fantasypoints + twopoint_fantasypoints)
                fantasy_points = fantasy_points/17
                return fantasy_points
    return None


def get_player_team_stats(player_team_id, teams_list):
    """
    Fetches the player team stats for the given player team ID.
    """
    for team in teams_list['body']:
        if team.get('teamAbv') == player_team_id:
            team_wins = int(team.get('wins'))
            team_losses = int(team.get('loss'))
            if team['currentStreak'].get('result') == "W":
                streak_factor = int(team['currentStreak'].get('length'))

            else:
                streak_factor = 1
            if team_losses == 0 or team_wins == 0:
                multiplier = team_wins * .01
                multiplier = multiplier * (streak_factor / 2) + 1
                return multiplier
            elif team_losses == 1:
                multiplier = (team_wins - 1) * .01
                multiplier = multiplier * (streak_factor / 2) + 1
                return multiplier
            else:
                multiplier = (team_wins/team_losses) * .01
                multiplier = multiplier * (streak_factor / 2) + 1
                return multiplier

    return None


def get_player_matchup_stats(team_id, week, player_pos, recent_games):
    weekly_matchups = get_nfl_games_for_week(week=week, season_type="reg", season="2024")
    opponent = ''
    for game in weekly_matchups['body']:
        if game['home'] == team_id or game['away'] == team_id:
            if game['home'] == team_id:
                opponent = game['away']
            else:
                opponent = game['home']
    schedules = get_nfl_teams(sort_by=opponent, rosters=False, schedules=False, top_performers=False,
                              team_stats=True, team_stats_season=2024)
    for team in schedules['body']:
        if team['teamAbv'] == opponent:
            if player_pos == 'QB':
                team_passtd_allowed = float(team['teamStats']['Defense']['passingTDAllowed'])
                team_passing_yards_allowed = float(team['teamStats']['Defense']['passingYardsAllowed'])
                team_defensive_interceptions = float(team['teamStats']['Defense']['defensiveInterceptions'])
                season_position_points = float((team_passing_yards_allowed*.04) +
                                               (team_passtd_allowed*4) - (team_defensive_interceptions*2))
                average_rushing_points = 0
                for game in recent_games['body']:
                    if 'Rushing' in recent_games['body'][game]:
                        rushing_gamepoints = float(recent_games['body'][game]['Rushing'].get('rushYds'))
                        average_rushing_points += rushing_gamepoints
                average_rushing_points = float((average_rushing_points/(week - 1))*.1)
                return (season_position_points / (week - 1)) + average_rushing_points

            elif player_pos == 'WR':
                team_passtd_allowed = float(team['teamStats']['Defense']['passingTDAllowed'])
                team_passing_yards_allowed = float(team['teamStats']['Defense']['passingYardsAllowed'])
                season_position_points = float((team_passing_yards_allowed*.1) + (team_passtd_allowed*6))
                average_rushing_points = 0
                average_throwing_points = 0
                average_touchdown_points = 0
                for game in recent_games['body']:
                    if 'Rushing' in recent_games['body'][game]:
                        rushing_gamepoints = float(recent_games['body'][game]['Rushing'].get('rushYds'))
                        average_rushing_points += rushing_gamepoints
                    if 'Passing' in recent_games['body'][game]:
                        throwing_gamepoints = float(recent_games['body'][game]['Passing'].get('passYds'))
                        touchdown_gamepoints = float(recent_games['body'][game]['Passing'].get('passTD'))
                        average_throwing_points += throwing_gamepoints
                        average_touchdown_points += touchdown_gamepoints
                average_rushing_points = float((average_rushing_points / (week - 1)) * .1)
                average_throwing_points = float((average_throwing_points / (week - 1)) * .04)
                average_touchdown_points = float((average_touchdown_points / (week - 1)) * 4)
                return ((season_position_points / (week - 1) / 2) + average_rushing_points +
                        average_throwing_points + average_touchdown_points)

            elif player_pos == 'RB':
                team_rushtd_allowed = float(team['teamStats']['Defense']['rushingTDAllowed'])
                team_rushing_yards_allowed = float(team['teamStats']['Defense']['rushingYardsAllowed'])
                season_position_points = float((team_rushing_yards_allowed*.1) + (team_rushtd_allowed*6))
                average_receiving_points = 0
                average_throwing_points = 0
                average_touchdown_points = 0
                for game in recent_games['body']:
                    if 'Receiving' in recent_games['body'][game]:
                        receiving_yardpoints = float(recent_games['body'][game]['Receiving'].get('recYds'))
                        receiving_points = float(recent_games['body'][game]['Receiving'].get('receptions'))
                        receiving_td = float(recent_games['body'][game]['Receiving'].get('recTD'))
                        average_receiving_points = (average_receiving_points + (receiving_yardpoints*.1) +
                                                    receiving_points + (receiving_td * 6))
                    else:
                        average_receiving_points += 0
                    if 'Passing' in recent_games['body'][game]:
                        throwing_gamepoints = float(recent_games['body'][game]['Passing'].get('passYds'))
                        touchdown_gamepoints = float(recent_games['body'][game]['Passing'].get('passTD'))
                        average_throwing_points += throwing_gamepoints
                        average_touchdown_points += touchdown_gamepoints
                average_receiving_points = average_receiving_points / (week - 1)
                average_throwing_points = float((average_throwing_points / (week - 1)) * .04)
                average_touchdown_points = float((average_touchdown_points / (week - 1)) * 4)
                return (season_position_points/(week-1) + average_receiving_points +
                        average_touchdown_points + average_throwing_points)

            elif player_pos == 'TE':
                team_passtd_allowed = float(team['teamStats']['Defense']['passingTDAllowed'])
                team_passing_yards_allowed = float(team['teamStats']['Defense']['passingYardsAllowed'])
                season_position_points = float((team_passing_yards_allowed * .1) + (team_passtd_allowed * 6))
                return season_position_points/(week-1) / 3
            else:
                return None
    return None


def get_player_pos(player_projections):
    position = player_projections['body']['pos']
    return position


def get_player_headshot(player_name):
    headshot, team = get_nfl_player_headshot(player_name)
    return headshot, team


def get_player_team(player_projections):
    player_team_id = str(player_projections['body'].get('team'))
    return player_team_id


def get_team_logo(team_name):
    # Fetch the NFL teams data
    data = get_nfl_teams()

    if data is None:
        print("Failed to retrieve team data.")
        return

    # Loop through the teams and find the one matching the given team name
    for team in data['body']:
        if team['teamAbv'].lower() == team_name.lower():
            logo_url = team['nflComLogo1']
            return logo_url

    print(f"Team '{team_name}' not found.")
    return None


# Calculate average fantasy points for the last set of games
def calculate_average_fantasy_points(games):
    total_points = 0
    for game in games['body']:
        gamepoints = float(games['body'][game]['fantasyPointsDefault'].get('PPR'))
        total_points += gamepoints
    return total_points


def get_player_stats(player_id):
    data = get_nfl_games_for_player(player_id)
    print(data)
    return None


def get_last_week_performance(games):
    points = 0
    if games['body']:
        first_game_key = next(iter(games['body']))
        first_game = games['body'][first_game_key]
        points = float(first_game['fantasyPointsDefault'].get('PPR', 0))
    return points
