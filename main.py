import pandas as pd
import requests
from acquire_data import get_full_data, pages_number, print_results
from data_wrangling import dataframing

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

#   print_results(data)
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(dataframing(data))
