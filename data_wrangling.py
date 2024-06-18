import pandas as pd
import matplotlib.pyplot as plt


def dataframing(data):
    df = pd.DataFrame(data)
    return df

def print_dataframe(data):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(data)

def boxplot(data):
    plt.boxplot(data['price'])
    plt.show()