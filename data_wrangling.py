import pandas as pd
import matplotlib


def dataframing(data):
    df = pd.DataFrame(data)
    #print(df['price'].mean())
    #print(df['price'].median())
    return df['flag']