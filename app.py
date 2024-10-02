from flask import Flask, render_template, request
from utils.comparison import compare_players, get_player_id, get_player_headshot, get_team_logo, get_player_pos
from utils.api_calls import get_fantasy_point_projections

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compare', methods=['POST'])
def compare():
    player_a_name = request.form.get('player_a')
    player_b_name = request.form.get('player_b')
    week = int(request.form.get('week'))

    # Get player IDs based on their names
    player_a_id = get_player_id(player_a_name)
    player_b_id = get_player_id(player_b_name)

    if not player_a_id or not player_b_id:
        result = "Error: Could not find one or both players."
        return render_template('index.html', result=result)

    # Fetch headshots for both players
    player_a_headshot, team1 = get_player_headshot(player_a_name)
    player_b_headshot, team2 = get_player_headshot(player_b_name)

    player_a_team_logo = get_team_logo(team1)
    player_b_team_logo = get_team_logo(team2)

    player_a_projections = get_fantasy_point_projections(player_id=player_a_id)
    player_b_projections = get_fantasy_point_projections(player_id=player_b_id)

    player_a_pos = get_player_pos(player_a_projections)
    player_b_pos = get_player_pos(player_b_projections)

    # Perform the comparison
    result = compare_players(player_a_id, player_b_id, week, player_a_name, player_b_name)

    # Pass the result and headshots back to the template for rendering
    return render_template(
        'index.html',
        result=result,
        player_a_name=player_a_name,
        player_b_name=player_b_name,
        player_a_headshot=player_a_headshot,
        player_b_headshot=player_b_headshot,
        player_a_team_logo=player_a_team_logo,
        player_b_team_logo=player_b_team_logo,
        player_a_pos=player_a_pos,
        player_b_pos=player_b_pos
    )


if __name__ == '__main__':
    app.run(debug=True)
