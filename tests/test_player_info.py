from utils.api_calls import get_nfl_player_info
import pandas as pd

#data = get_nfl_player_info(player_name="Hollywood Brown")
#print(data)
#print(data["body"][0]['injury'])
#if (data["body"][0]['injury'].get('designation') == ''):
    #print('yes')

csv_file_path = "nfl_fantasy_projections_wr.csv"
df = pd.read_csv(csv_file_path)

# Ensure "Season TDs Average" is treated as a numeric column
df["Season TDs Average"] = pd.to_numeric(df["Season TDs Average"], errors="coerce")

# Filter rows where "Season TDs Average" is at least 1
filtered_df = df[df["Season TDs Average"] >= .66]

# Display the filtered rows
print(filtered_df)