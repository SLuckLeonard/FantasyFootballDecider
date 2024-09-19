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
