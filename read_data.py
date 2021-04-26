import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_data():
    data_set = pd.read_csv("data/history/amandaeliselee.csv",
                           # sep=',',
                           # header=0,
                           # skiprows=0
                           )
    print(data_set.head(5))
