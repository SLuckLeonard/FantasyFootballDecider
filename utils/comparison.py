from utils.api_calls import get_fantasy_point_projections, get_nfl_teams, get_nfl_games_for_player


def compare_players(player_a_id, player_b_id, week):
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
    print(player_a_points)
    player_b_points = get_player_week_points(player_b_id)
    print(player_b_points)

    # 2. Get Team Performance
    teams = get_nfl_teams()
    if not teams:
        return "Error: Could not retrieve team information."

    player_a_team_id = player_a_projections['playerProjections'][str(player_a_id)]['teamID']
    player_b_team_id = player_b_projections['playerProjections'][str(player_b_id)]['teamID']

    # Extract team performance (e.g., win/loss record, standings)
    player_a_team_stats = next((team for team in teams['teams'] if team['teamID'] == player_a_team_id), None)
    player_b_team_stats = next((team for team in teams['teams'] if team['teamID'] == player_b_team_id), None)

    if not player_a_team_stats or not player_b_team_stats:
        return "Error: Could not retrieve team stats for one or both players."

    # Simple score using team wins
    player_a_team_performance = float(player_a_team_stats['teamStats']['wins'])
    player_b_team_performance = float(player_b_team_stats['teamStats']['wins'])

    # 3. Get Recent Player Performance
    player_a_recent_games = get_nfl_games_for_player(player_a_id, number_of_games=3)  # Last 3 games
    player_b_recent_games = get_nfl_games_for_player(player_b_id, number_of_games=3)

    if not player_a_recent_games or not player_b_recent_games:
        return "Error: Could not retrieve recent game data for one or both players."

    # Calculate average fantasy points for the last 3 games
    def calculate_average_fantasy_points(games):
        total_points = 0
        game_count = len(games['games'])
        for game in games['games']:
            total_points += float(game['fantasyPoints'])
        return total_points / game_count if game_count > 0 else 0

    player_a_recent_performance = calculate_average_fantasy_points(player_a_recent_games)
    player_b_recent_performance = calculate_average_fantasy_points(player_b_recent_games)

    # 4. Calculate Final Scores
    # Weighted score: 50% on fantasy projection, 25% on team performance, and 25% on recent performance
    def calculate_score(fantasy_points, team_performance, recent_performance):
        return (fantasy_points * 0.5) + (team_performance * 0.25) + (recent_performance * 0.25)

    player_a_score = calculate_score(player_a_points, player_a_team_performance, player_a_recent_performance)
    player_b_score = calculate_score(player_b_points, player_b_team_performance, player_b_recent_performance)

    # 5. Compare and Return the Result
    if player_a_score > player_b_score:
        return f"Start Player A (ID: {player_a_id}) with a score of {player_a_score:.2f} over Player B (ID: {player_b_id}) with a score of {player_b_score:.2f}"
    else:
        return f"Start Player B (ID: {player_b_id}) with a score of {player_b_score:.2f} over Player A (ID: {player_a_id}) with a score of {player_a_score:.2f}"

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