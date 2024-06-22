from progress_bar import progress
from bs4 import BeautifulSoup
from acquire_data import get_soup

def get_full_single_product(link_list):
    result = []
    for link in link_list:
        soup = get_soup(link)
        result += [get_single_data(soup)]
    return result

def get_single_data(soup):
    # Name
    name = soup.find('div', {'class': 'name'}).text

    # Price and Standard Price in PLN
    prices = soup.find('div', {'class': 'price'}).find_all('span')
    # Standard price is a price without price drop
    if len(prices) == 3:
        # \u2009 is a light space for thousands serparation. 
        standard_price = prices[2].text[:-3].replace('\u2009', '').replace(',', '.')
        price = prices[0].text[:-3].replace('\u2009', '').replace(',', '.')
    else:
        standard_price = 0
        price = prices[0].text[:-3].replace('\u2009', '').replace(',', '.')

    # Flags
    flags = None

    # Dimensions
    dimensions = soup.find('div', {'class': 'dimensions'}).find_all('div', {'class': 'item'})
    
    # Index
    index = soup.find('div', {'class': 'product-code'}).text.split(' ')[1]

    # Color
    try:
        color = soup.find('div', {'id': 'other-colors'}).find('div', {'class': 'current-name'}).text
    except: color = None

    # Ratings 
    try:
        rating_div = soup.find('div', {'class': 'rating'})
        rating = rating_div('span', {'class': 'value'}).text[2:5]

        # Ratings count
        rating_count = rating_div.find('span', {'class': 'quantity'}).text
    except: 
        rating = None 
        rating_count = None

    return {'name': name, 'price': float(price), 'standard_price': float(standard_price), 'flags': flags, 'dimensions': dimensions, 'index': index, 'color': color, 'rating': rating, 'rating_count': rating_count}

