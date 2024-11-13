from utils.make_csv import add_data_to_csv, create_csv

CSV_FILE_WR = 'nfl_fantasy_projections_wr.csv'
CSV_FILE_TE = 'nfl_fantasy_projections_te.csv'
CSV_FILE_RB = 'nfl_fantasy_projections_rb.csv'
CSV_FILE_QB = 'nfl_fantasy_projections_qb.csv'
CSV_FILE_PK = 'nfl_fantasy_projections_pk.csv'

if __name__ == "__main__":
    create_csv(CSV_FILE_WR, 'WR')
    #create_csv(CSV_FILE_TE, 'TE')
    #create_csv(CSV_FILE_RB, 'RB')
    #create_csv(CSV_FILE_QB, 'QB')
    #create_csv(CSV_FILE_PK, 'PK')
    add_data_to_csv(CSV_FILE_WR, 'WR')
    #add_data_to_csv(CSV_FILE_RB, 'RB')
    #add_data_to_csv(CSV_FILE_QB, 'QB')
    #add_data_to_csv(CSV_FILE_TE, 'TE')
    #add_data_to_csv(CSV_FILE_PK, 'PK')

