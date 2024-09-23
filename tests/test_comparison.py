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

    breece_hall_id = get_player_id("Breece Hall")
    bijan_robinson_id = get_player_id("Bijan Robinson")

    if ladd_mcconkey_id and xavier_worthy_id:
        print(f"Found Breece Hall's ID: {breece_hall_id}")
        print(f"Found Bijan Robinson's ID: {bijan_robinson_id}")

        print(compare_players(breece_hall_id, bijan_robinson_id, 4))
    else:
        print("Failed to retrieve player IDs for Breece Hall and Bijan Robinson")

    brock_bowers_id = get_player_id("Brock Bowers")
    travis_kelce_id = get_player_id("Travis Kelce")

    if brock_bowers_id and travis_kelce_id:
        print(f"Found Brock Bowers' ID: {brock_bowers_id}")
        print(f"Found Travis Kelce's ID: {travis_kelce_id}")

        print(compare_players(brock_bowers_id, travis_kelce_id, 4))
    else:
        print("Failed to retrieve player IDs for Brock Bowers and Travis Kelce")
