import requests
from bs4 import BeautifulSoup

def get_config(conf):
    with open('config.txt') as config:
        contents = [line for line in config]
        URL = contents[1]
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
            price = o.find('div', {'class': 'price'}).find('span').text[:-3].replace('\u2009', '')
            dimensions = o.find('div', {'class': 'dimensions'})
            result += [{'name': name, 'price': int(price), 'dimensions': dimensions}]
        except:
            continue
    return result

def print_results(res):
    for x in res:
        print(x)
    print(len(res))

URL = get_config('URL')
page_num = pages_number(URL)


#for i in page_num:
#    pass


if __name__ == "__main__":
    print_results(get_data(URL))

