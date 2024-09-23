from utils.comparison import compare_players, get_player_id




if __name__ == "__main__":
    # Get player IDs
    aaron_rodgers_id = get_player_id("Aaron Rodgers")
    patrick_mahomes_id = get_player_id("Patrick Mahomes")

    if aaron_rodgers_id and patrick_mahomes_id:
        print(f"Found Aaron Rodgers' ID: {aaron_rodgers_id}")
        print(f"Found Patrick Mahomes' ID: {patrick_mahomes_id}")

        # Compare Aaron Rodgers and Patrick Mahomes
        print(compare_players(aaron_rodgers_id, patrick_mahomes_id, 4))
    else:
        print("Failed to retrieve player IDs for Aaron Rodgers or Patrick Mahomes.")

    ladd_mcconkey_id = get_player_id("Ladd McConkey")
    xavier_worthy_id = get_player_id("Xavier Worthy")

    if ladd_mcconkey_id and xavier_worthy_id:
        print(f"Found Ladd McConkey's ID: {ladd_mcconkey_id}")
        print(f"Found Xavier Worthy's ID: {xavier_worthy_id}")

        print(compare_players(ladd_mcconkey_id, xavier_worthy_id, 4))
    else:
        print("Failed to retrieve player IDs for Ladd McConkey and Xavier Worthy")
