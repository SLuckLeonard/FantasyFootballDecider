from utils.api_calls import get_fantasy_point_projections, get_nfl_teams, get_nfl_games_for_player, get_nfl_games_for_week


def compare_players(player_a_id, player_b_id, week, player_a_name, player_b_name):
    """
    Compares two NFL players based on fantasy point projections, team performance, and recent stats.

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

    player_a_team_id = str(player_a_projections['body'].get('team'))
    player_b_team_id = str(player_b_projections['body'].get('team'))

    # Extract team performance (e.g., win/loss record, standings)
    player_a_team_stats = get_player_team_stats(player_a_team_id, teams)
    #print(player_a_team_stats)
    player_b_team_stats = get_player_team_stats(player_b_team_id, teams)
    #print(player_b_team_stats)

    if not player_a_team_stats or not player_b_team_stats:
        return "Error: Could not retrieve team stats for one or both players."

    player_a_updated_proj = player_a_points * player_a_team_stats
    player_b_updated_proj = player_b_points * player_b_team_stats

    # 3. Get Recent Player Performance
    player_a_recent_games = get_nfl_games_for_player(player_a_id, number_of_games=week-1)
    player_b_recent_games = get_nfl_games_for_player(player_b_id, number_of_games=week-1)

    if not player_a_recent_games or not player_b_recent_games:
        return "Error: Could not retrieve recent game data for one or both players."

    # Calculate average fantasy points for the last 3 games
    def calculate_average_fantasy_points(games):
        total_points = 0
        for game in games['body']:
            gamepoints = float(games['body'][game].get('fantasyPoints'))
            total_points += gamepoints
        return total_points

    player_a_season_performance = calculate_average_fantasy_points(player_a_recent_games)/(week - 1)
    player_b_season_performance = calculate_average_fantasy_points(player_b_recent_games)/(week - 1)

    # 4. Calculate Final Scores
    player_a_solo_pred_score = (player_a_updated_proj + player_a_season_performance)/2
    player_b_solo_pred_score = (player_b_updated_proj + player_b_season_performance)/2

    # 5. Calculate opponent toughness
    player_a_position = get_player_pos(player_a_projections)
    player_b_position = get_player_pos(player_b_projections)
    player_a_matchup_avg_points_allowed = get_player_matchup_stats(player_a_team_id, week, player_a_position)
    player_b_matchup_avg_points_allowed = get_player_matchup_stats(player_b_team_id, week, player_b_position)

    # 6. Take Final Scores with opponent toughness
    player_a_score = float((player_a_solo_pred_score + player_a_matchup_avg_points_allowed)/2)
    print(player_a_score)
    player_b_score = float((player_b_solo_pred_score + player_b_matchup_avg_points_allowed)/2)
    print(player_b_score)

    # 5. Compare and Return the Result
    if player_a_score > player_b_score:
        return f"Start Player A (ID: {player_a_name}) with a score of {player_a_score:.2f} over Player B (ID: {player_b_name}) with a score of {player_b_score:.2f}"
    else:
        return f"Start Player B (ID: {player_b_name}) with a score of {player_b_score:.2f} over Player A (ID: {player_a_name}) with a score of {player_a_score:.2f}"

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

def get_player_week_points(player_ID):
    """
    Fetches the player avg points for the given playerID.
    """
    data = get_fantasy_point_projections(week='season')

    if data and 'body' in data:
        projections = data['body'].get('playerProjections', [])
        for player in projections:
            if player == player_ID:
                rush_fantasypoints = float(projections[player]['Rushing'].get('rushYds'))/10 + float(projections[player]['Rushing'].get('rushTD'))*6
                pass_fantasypoints = float(projections[player]['Passing'].get('passYds'))*.04 + float(projections[player]['Passing'].get('passTD'))*4 - float(projections[player]['Passing'].get('int'))*2
                receiving_fantasypoints = float(projections[player]['Receiving'].get('recTD'))*6 + float(projections[player]['Receiving'].get('receptions')) + float(projections[player]['Receiving'].get('recYds'))*.01
                fumble_fantasypoints = float(projections[player].get('fumblesLost'))*2
                twoPoint_fantasypoints = float(projections[player].get('twoPointConversion')) * 2
                fantasy_points = rush_fantasypoints + pass_fantasypoints + receiving_fantasypoints - fumble_fantasypoints + twoPoint_fantasypoints
                fantasy_points = fantasy_points/17
                return fantasy_points
    return None

def get_player_team_stats(player_team_id, teams_list):
    """
    Fetches the player team stats for the given player team ID.
    """
    for team in teams_list['body']:
        if team.get('teamAbv') == player_team_id:
            multiplier = 0
            team_wins = int(team.get('wins'))
            team_losses = int(team.get('loss'))
            if team['currentStreak'].get('result') == "W":
                streakFactor = int(team['currentStreak'].get('length'))
                #print("streakFactor=", streakFactor)
            else:
                streakFactor = 1
            if team_losses == 0 or team_wins == 0:
                multiplier = team_wins * .01
                multiplier = multiplier * (streakFactor / 2) + 1
                return multiplier
            elif team_losses == 1:
                multiplier = (team_wins - 1) * .01
                multiplier = multiplier * (streakFactor / 2) + 1
                return multiplier
            else:
                multiplier = (team_wins/team_losses) * .01
                multiplier = multiplier * (streakFactor / 2) + 1
                return multiplier

    return None

def get_player_matchup_stats(team_id, week, player_pos):
    weekly_matchups = get_nfl_games_for_week(week=week, season_type="reg", season="2024")
    opponent = ''
    for game in weekly_matchups['body']:
        if game['home'] == team_id or game['away'] == team_id:
            if game['home'] == team_id:
                opponent = game['away']
            else:
                opponent = game['home']
    schedules = get_nfl_teams(sort_by=opponent, rosters=False, schedules=False, top_performers=False, team_stats=True, team_stats_season=2024)
    for team in schedules['body']:
        if team['teamAbv'] == opponent:
            if player_pos == 'QB':
                team_passTDAllowed = float(team['teamStats']['Defense']['passingTDAllowed'])
                team_passingYardsAllowed = float(team['teamStats']['Defense']['passingYardsAllowed'])
                team_defensiveInterceptions = float(team['teamStats']['Defense']['defensiveInterceptions'])
                season_position_points = float((team_passingYardsAllowed*.04) + (team_passTDAllowed*4) - (team_defensiveInterceptions*2))
                return season_position_points/(week-1) + 5

            elif player_pos == 'WR':
                team_passTDAllowed = float(team['teamStats']['Defense']['passingTDAllowed'])
                team_passingYardsAllowed = float(team['teamStats']['Defense']['passingYardsAllowed'])
                season_position_points = float((team_passingYardsAllowed*.1) + (team_passTDAllowed*6))
                return season_position_points/(week-1) / 2

            elif player_pos == 'RB':
                team_rushTDAllowed = float(team['teamStats']['Defense']['rushingTDAllowed'])
                team_rushingYardsAllowed = float(team['teamStats']['Defense']['rushingYardsAllowed'])
                season_position_points = float((team_rushingYardsAllowed*.1) + (team_rushTDAllowed*6))
                return season_position_points/(week-1) + 5

            elif player_pos == 'TE':
                team_passTDAllowed = float(team['teamStats']['Defense']['passingTDAllowed'])
                team_passingYardsAllowed = float(team['teamStats']['Defense']['passingYardsAllowed'])
                season_position_points = float((team_passingYardsAllowed * .1) + (team_passTDAllowed * 6))
                return season_position_points/(week-1) / 3
            else:
                return None


    return None


def get_player_pos(player_projections):
    position = player_projections['body']['pos']
    return position

