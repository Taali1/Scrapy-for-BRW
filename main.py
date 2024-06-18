import requests
from bs4 import BeautifulSoup
import pandas as pd
from progress_bar import progress

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

def get_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def pages_number(url) -> int:
    soup = get_soup(url)
    pages = soup.find('div', {'class': 'pager-quantity-wrapper'})
    return int(pages.find('a', {'title': 'Ostatnia strona'}).text)

def get_data(url):
    result = []
    soup = get_soup(url)
    products = soup.find_all('div', {'class': 'single-product'})
    for o in products:
        # Just skips if thers an error because im too lazy and dont want to overcomplicate this code.
        # There're product divs that play role as ad board and this doesnt contain any data so bs4 is throwing out errors
        try:
            name = o.find('h3').text
            # Price in PLN
            prices = o.find('div', {'class': 'price'}).find_all('span')
            # Standard price is a price without price drop, i should add scrapping promo tags
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

def get_full_data(url, num, limit = None):
    result = []
    print(f'Theres {num} pages')
    print(f'Importing {limit} of them')
    for i in range(num+1)[1:limit]:
        result += get_data(url+str(i))
        progress(i, num if limit == None else limit-1, 40)
    return result

if __name__ == "__main__":
    URL = get_config('URL')
    limit = get_config('limit')
    page_num = pages_number(URL)
    
    data = get_full_data(URL, page_num, limit)

    df = pd.DataFrame(data)
    print(df['price'].mean())
    print(df['price'].median())

