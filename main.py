import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_config(conf):
    with open('config.txt') as config:
        contents = [line for line in config]
        URL = contents[1][:-1]
    match conf:
        case 'URL':
            return URL

def get_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def pages_number(url) -> int:
    soup = get_soup(url)
    pages = soup.find('div', {'class': 'pager-quantity-wrapper'})
    return pages.find('a', {'title': 'Ostatnia strona'}).text

def get_data(url):
    result = []
    soup = get_soup(url)
    products = soup.find_all('div', {'class': 'single-product'})
    for o in products:
        try:
            name = o.find('h3').text
            # Price in PLN
            prices = o.find('div', {'class': 'price'}).find_all('span')
            if len(prices) == 3:
                standard_price = prices[2].text[:-3].replace('\u2009', '')
                price = prices[0].text[:-3].replace('\u2009', '')
            else:
                standard_price = 0
                price = prices[0].text[:-3].replace('\u2009', '')
            dimensions = o.find('div', {'class': 'dimensions'})
            result += [{'name': name, 'price': int(price), 'standard_price': int(standard_price), 'dimensions': dimensions}]
        except:
            continue
    return result

def print_results(res):
    for x in res:
        print(x)
    print(len(res))

def get_full_data(url, num):
    result = []
    for i in num:
        result += get_data(URL+i)
    return result

if __name__ == "__main__":
    URL = get_config('URL')
    page_num = pages_number(URL)
    
    data = get_full_data(URL, page_num)

    df = pd.DataFrame(data)
    print(df['price'].mean())
    print(df['price'].median())

