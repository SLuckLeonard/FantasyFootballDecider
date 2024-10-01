from utils.comparison import get_player_id, get_player_headshot

if __name__ == "__main__":
    # Get player IDs

    id1 = get_player_headshot("Aaron Rodgers")
    id2 = get_player_headshot("Patrick Mahomes")

    print(id1, id2)

