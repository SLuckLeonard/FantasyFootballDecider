import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# RapidAPI credentials
RAPIDAPI_HOST = "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # Make sure you set this in your .env file

# Base URL for NFL projections
BASE_URL = f"https://{RAPIDAPI_HOST}/getNFLProjections"
BASE_TEAM_URL = f"https://{RAPIDAPI_HOST}/getNFLTeams"
BASE_PLAYER_STATS_URL = f"https://{RAPIDAPI_HOST}/getNFLGamesForPlayer"
BASE_WEEKLY_GAMES_URL = f"https://{RAPIDAPI_HOST}/getNFLGamesForWeek"
BASE_PLAYER_INFO_URL = f"https://{RAPIDAPI_HOST}/getNFLPlayerInfo"


def get_fantasy_point_projections(week='season', archive_season=2024, player_id=None, team_id=None, **scoring_params):
    """
    Fetches fantasy point projections for NFL players.

    :param week: The week number (1-18) or 'season' for full season projections.
    :param archive_season: The year to fetch projections for (e.g., 2024).
    :param player_id: The player ID to filter projections for a specific player.
    :param team_id: The team ID to filter projections for a specific team.
    :param scoring_params: Additional scoring rules like twoPointConversions, passYards, etc.
    :return: A JSON response with the projections.
    """

    # Set up the query parameters
    params = {
        'week': week,
        'archiveSeason': archive_season,
        **scoring_params  # Include custom scoring parameters
    }

    if player_id:
        params['playerID'] = player_id
    elif team_id:
        params['teamID'] = team_id

    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY,
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for 4XX/5XX errors
        data = response.json()
        return data  # You can further process this data if needed

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return None


def get_nfl_teams(sort_by="standings", rosters=False, schedules=False, top_performers=True,
                  team_stats=True, team_stats_season=2023):
    """
    Fetches NFL team information with optional parameters.

    :param sort_by: Sort by standings or teamID (default: standings).
    :param rosters: Whether to retrieve rosters for the teams (default: False).
    :param schedules: Whether to retrieve schedules for the teams (default: False).
    :param top_performers: Retrieve the best player in each category for each team (default: True).
    :param team_stats: Retrieve season-long team statistics (default: True).
    :param team_stats_season: Season year for team statistics (default: 2023).
    :return: A JSON response with team information and statistics.
    """

    # Set up the query parameters
    params = {
        'sortBy': sort_by,
        'rosters': str(rosters).lower(),  # Convert to string ('true'/'false')
        'schedules': str(schedules).lower(),
        'topPerformers': str(top_performers).lower(),
        'teamStats': str(team_stats).lower(),
        'teamStatsSeason': team_stats_season,
    }

    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY,
    }

    try:
        response = requests.get(BASE_TEAM_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data  # You can further process this data if needed

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return None


def get_nfl_games_for_player(player_id, fantasy_points=True, number_of_games=None, two_point_conversions=2,
                             pass_yards=0.04, pass_td=4, pass_interceptions=-2, points_per_reception=1,
                             carries=0.2, rush_yards=0.1, rush_td=6, fumbles=-2, receiving_yards=0.1,
                             receiving_td=6, targets=0, def_td=6, xp_made=1, xp_missed=-1, fg_made=3,
                             fg_missed=-3, season=None):
    """
    Fetches NFL game stats for a specific player.

    :param player_id: The unique player ID (required).
    :param fantasy_points: Whether to calculate fantasy points (default: True).
    :param number_of_games: Limit the number of recent games returned (optional).
    :param season: Season year (optional).
    :param two_point_conversions: Fantasy points for two-point conversions (default: 2).
    :param pass_yards: Fantasy points per passing yard (default: 0.04).
    :param pass_td: Fantasy points per passing touchdown (default: 4).
    :param pass_interceptions: Fantasy points penalty for interceptions (default: -2).
    :param points_per_reception: Points per reception (default: 1).
    :param carries: Points per carry (default: 0.2).
    :param rush_yards: Points per rushing yard (default: 0.1).
    :param rush_td: Points per rushing touchdown (default: 6).
    :param fumbles: Fantasy points penalty for fumbles (default: -2).
    :param receiving_yards: Points per receiving yard (default: 0.1).
    :param receiving_td: Points per receiving touchdown (default: 6).
    :param targets: Points per target (default: 0).
    :param def_td: Points per defensive touchdown (default: 6).
    :param xp_made: Points for extra points made (default: 1).
    :param xp_missed: Penalty for extra points missed (default: -1).
    :param fg_made: Points per field goal made (default: 3).
    :param fg_missed: Penalty for field goal missed (default: -3).
    :return: A JSON response with the player's game stats.
    """

    # Set up the query parameters
    params = {
        'playerID': player_id,
        'fantasyPoints': str(fantasy_points).lower(),
        'twoPointConversions': two_point_conversions,
        'passYards': pass_yards,
        'passTD': pass_td,
        'passInterceptions': pass_interceptions,
        'pointsPerReception': points_per_reception,
        'carries': carries,
        'rushYards': rush_yards,
        'rushTD': rush_td,
        'fumbles': fumbles,
        'receivingYards': receiving_yards,
        'receivingTD': receiving_td,
        'targets': targets,
        'defTD': def_td,
        'xpMade': xp_made,
        'xpMissed': xp_missed,
        'fgMade': fg_made,
        'fgMissed': fg_missed,
    }

    if number_of_games:
        params['numberOfGames'] = number_of_games

    if season:
        params['season'] = season

    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY,
    }

    try:
        response = requests.get(BASE_PLAYER_STATS_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data  # You can further process this data if needed

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return None


def get_nfl_games_for_week(week, season_type="reg", season=None):
    """
    Fetches NFL games for a given week in a specific season.

    :param week: The NFL week number (1-18) or 'all' to get all games for the season.
    :param season_type: The type of season ('reg', 'post', 'pre', or 'all'). Default is 'reg'.
    :param season: The year of the NFL season (e.g., 2024). If not specified, defaults to current season.
    :return: A JSON response with game details for the specified week.
    """

    # Set up the query parameters
    params = {
        'week': week,
        'seasonType': season_type,
    }

    if season:
        params['season'] = season

    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY,
    }

    try:
        # Perform the GET request
        response = requests.get(BASE_WEEKLY_GAMES_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()  # Parse the JSON response
        return data  # Return the game data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return None


def get_nfl_player_headshot(player_name, get_stats=True):
    """
    Fetches an NFL player's ESPN headshot based on their name.

    :param player_name: The player's name (e.g., 'keenan_a' for Keenan Allen).
    :param get_stats: Whether to retrieve player stats as well (default: True).
    :return: The URL of the player's ESPN headshot, or None if not found.
    """
    # Set up the query parameters
    params = {
        'playerName': player_name,
        'getStats': str(get_stats).lower(),  # Convert to string ('true'/'false')
    }

    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY,
    }

    try:
        # Perform the GET request
        response = requests.get(BASE_PLAYER_INFO_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()

        # Extract ESPN headshot URL
        espn_headshot = data['body'][0].get('espnHeadshot')

        # Extract Team name
        team_name = data['body'][0].get('team')

        if espn_headshot:
            return espn_headshot, team_name
        else:
            print(f"No headshot found for player: {player_name}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return None


def get_nfl_player_info(player_name=None, player_id=None, get_stats=True):
    """
    Fetches detailed information for an NFL player based on player name or ID.

    :param player_name: The player's name (e.g., 'keenan_a' for Keenan Allen, optional).
    :param player_id: The player's unique ID (optional).
    :param get_stats: Whether to retrieve current season stats (default: True).
    :return: A JSON response with player information and stats if available.
    """

    # Set up the query parameters
    params = {
        'getStats': str(get_stats).lower()  # Convert to string ('true'/'false')
    }

    # Add player-specific parameters if provided
    if player_name:
        params['playerName'] = player_name
    if player_id:
        params['playerID'] = player_id

    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY,
    }

    try:
        # Perform the GET request
        response = requests.get(BASE_PLAYER_INFO_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse and return JSON response
        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return None
