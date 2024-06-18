import pandas as pd
from acquire_data import get_full_data, pages_number
from data_wrangling import dataframing, boxplot

def get_config(conf):
    with open('config.txt') as config:
        contents = [line for line in config]
        URL = contents[1][:-1]
        limit = contents[3]
    match conf:
        case 'URL':
            return URL
        case 'limit':
            return int(limit)

if __name__ == "__main__":
    URL = get_config('URL')
    limit = get_config('limit')

    page_num = pages_number(URL)
    
    data = get_full_data(URL, page_num, limit)

    df = dataframing(data)

    df.to_csv('brw.csv')
    print('Saved dataframe to .csv file')

    #boxplot(dataframing(data))
