import pandas as pd
from pathlib import Path



def get_trips_in_Switzerland(year, selected_columns=None):
    if year == 2015:
        folder_path = Path('../data/input/')
        with open(folder_path / 'wegeinland.csv', 'r') as trips_in_Switzerland_file:
            df_trips_in_Switzerland = pd.read_csv(trips_in_Switzerland_file,
                                                  delimiter=',',
                                                  usecols=selected_columns,
                                                  na_values=[-99])
    else:
        raise Exception('Year not well defined')
    return df_trips_in_Switzerland


def get_zp(year, selected_columns=None):
    if year == 2015:
        folder_path = Path('../data/input/')
        with open(folder_path / 'zielpersonen.csv', 'r') as zielpersonen_file:
            if selected_columns is None:
                df_zp = pd.read_csv(zielpersonen_file)
            else:
                df_zp = pd.read_csv(zielpersonen_file,
                                    dtype={'HHNR': int},
                                    usecols=selected_columns)
    else:
        raise Exception('Year not well defined')
    return df_zp