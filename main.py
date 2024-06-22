import pandas as pd
from acquire_data import get_full_data, pages_number, get_soup
from data_wrangling import dataframing, boxplot, print_dataframe
from acquire_single_data import get_single_data
import json

def get_config():
   with open('config.json') as file:
        config = json.load(file)
   return config

if __name__ == "__main__":
    config = get_config()
    
    '''
    URL = config["url"]
    limit = config["limit"]
    
    page_num = pages_number(URL)
    
    data = get_full_data(URL, page_num, limit)

    df = dataframing(data)

    print(df)

    df.to_csv('brw.csv')
    print('Saved dataframe to .csv file')

    #boxplot(dataframing(data))
    '''
    data = get_single_data(get_soup('https://www.brw.pl/szafa-pieciodrzwiowa-stockholm-243-cm-sosna-andersen-biala,15022'))
    print(dataframing(data))