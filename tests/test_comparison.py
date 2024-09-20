from utils.comparison import compare_players, get_player_id




if __name__ == "__main__":
    # Get player IDs
    aaron_rodgers_id = get_player_id("Aaron Rodgers")
    patrick_mahomes_id = get_player_id("Patrick Mahomes")

    if aaron_rodgers_id and patrick_mahomes_id:
        print(f"Found Aaron Rodgers' ID: {aaron_rodgers_id}")
        print(f"Found Patrick Mahomes' ID: {patrick_mahomes_id}")

        # Compare Aaron Rodgers and Patrick Mahomes
        compare_players(aaron_rodgers_id, patrick_mahomes_id, 'Week_3')
    else:
        print("Failed to retrieve player IDs for Aaron Rodgers or Patrick Mahomes.")
