from utils.comparison import get_player_headshot, get_team_logo, get_player_stats, get_player_id

if __name__ == "__main__":

    team_id1, team1 = get_player_headshot("Aaron Rodgers")
    team_id2, team2 = get_player_headshot("Patrick Mahomes")

    player_a_id = get_player_id("Aaron Rodgers")
    player_b_id = get_player_id("Patrick Mahomes")

    print(team_id1, team1, team_id2, team2)

    team1_logo = get_team_logo(team1)
    team2_logo = get_team_logo(team2)

    print(team1_logo, team2_logo)

    get_player_stats(player_a_id)
