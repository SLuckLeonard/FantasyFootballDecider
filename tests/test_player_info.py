from utils.api_calls import get_nfl_player_info


data = get_nfl_player_info(player_name="Hollywood Brown")
#print(data)
print(data["body"][0]['injury'])
if (data["body"][0]['injury'].get('designation') == ''):
    print('yes')