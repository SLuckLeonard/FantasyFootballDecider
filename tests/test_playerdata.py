from utils.comparison import get_player_headshot, get_team_logo

if __name__ == "__main__":

    id1, team1 = get_player_headshot("Aaron Rodgers")
    id2, team2 = get_player_headshot("Patrick Mahomes")

    print(id1, team1, id2, team2)

    team1_logo = get_team_logo(team1)
    team2_logo = get_team_logo(team2)

    print(team1_logo, team2_logo)
