from utils.api_calls import get_fantasy_point_projections

# Example: Get full season projections for 2024 with default scoring
projections = get_fantasy_point_projections()

# Example: Get projections for a specific player using player ID
player_projections = get_fantasy_point_projections(player_id="8439")

# Example: Customize scoring rules and get full season projections
custom_projections = get_fantasy_point_projections(
    passYards=0.04, passTD=4, passInterceptions=-2, rushTD=6
)

if projections:
    print(projections)
