import csv
import os
from api_calls import get_fantasy_point_projections

# CSV file path
CSV_FILE = 'nfl_fantasy_projections.csv'


# Create the CSV file and define its columns
def create_csv(file_path):
    # Define the column headers (adjust as per the API response structure)
    headers = ['Player Name', 'Week', 'Projected Points', 'Team']

    # Check if the file already exists to avoid overwriting
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            print(f"CSV file '{file_path}' created with headers: {headers}")
    else:
        print(f"CSV file '{file_path}' already exists.")


# Add a single row of data to the CSV from the API response
def add_data_to_csv(file_path):
    # Example API call to get fantasy point projections for a specific player
    player_id = 12345  # Example player ID
    week = 1  # Example week
    archive_season = 2024  # Example season

    # Fetch data from the API
    api_data = get_fantasy_point_projections(week=week, archive_season=archive_season, player_id=player_id)

    if api_data and 'body' in api_data:
        player_data = api_data['body'][0]  # Assuming 'body' contains a list of player projections

        # Extract the required fields for the CSV (modify based on actual API response)
        player_name = player_data.get('playerName', 'N/A')
        projected_points = player_data.get('projectedFantasyPoints', 'N/A')
        team = player_data.get('team', 'N/A')

        # Add the data as a new row
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, week, projected_points, team])
            print(f"Added row to CSV: {player_name}, {week}, {projected_points}, {team}")
    else:
        print("No data received from the API")


