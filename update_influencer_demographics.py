import pandas as pd
from mongo import update_demographics

if __name__ == '__main__':
    # read data
    df = pd.read_csv("data/influencer_demographics.csv",
                     sep=',',
                     header=0,
                     skiprows=0)

    #lower case
    df['sex'] = df.sex.astype(str).str.lower()
    df['marital_status'] = df.marital_status.astype(str).str.lower()
    df['category'] = df.category.astype(str).str.lower()

    print(df)
    update_demographics(df)
