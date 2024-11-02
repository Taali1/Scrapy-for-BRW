from progress_bar import progress
from bs4 import BeautifulSoup
import requests

def get_soup(url: str) -> str:
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

        if o.find('h3'):
            name = o.find('h3').text
            name = name.replace("\xa0", " ")
            split_name = name.split(' ')
            splited = ""
            try:
                for i in split_name:
                    if i == "RTV":
                        splited += f"{i} "

                    if i[0].isupper() or i[0].isnumeric():
                        break
                    else:
                        splited += f"{i} "
            except:
                continue
        else:
            continue
        # Price in PLN
        try:
            prices = o.find('div', {'class': 'price'}).find_all('span')
            # Standard price is a price without price drop
            if len(prices) == 3:
                # \u2009 is a light space for thousands serparation. 
                standard_price = prices[2].text[:-3].replace('\u2009', '').replace(',', '.')
                price = prices[0].text[:-3].replace('\u2009', '').replace(',', '.')
            else:
                standard_price = 0
                price = prices[0].text[:-3].replace('\u2009', '').replace(',', '.')
        except:
            standard_price = 0.0
            price = 0.0
        flag = get_flags(o)

        result += [{'name': name, 'price': price, 'standard_price': float(standard_price), 'flag': flag, 'category': splited.strip()}]
    return result

def get_full_data(url, num, limit = None):
    result = []
    print(f'Theres {num} pages')
    print(f'Importing {limit} of them')
    if limit < num:
        for i in range(num+1)[1:limit]:
            result += get_data(url+str(i))
            progress(i, num if limit == None else limit-1, 40)
    else: 
        for i in range(1, num+1):
            result += get_data(url+str(i))
            progress(i, num, 40)
    return result

def get_flags(product):
    results = []
    has_flags = product.find_all('div', {'class': 'new-promo-flags'})
    for has_flags in has_flags:
        # Promo flag
        try: results += [has_flags.find('span').text]
        except Exception: pass

        # Sale flag
        try: results += [has_flags.find('div', {'class': 'st_wyprzedaz'}).text.replace('\n', '').strip()]
        except Exception: pass

        # New
        try: results += [has_flags.find('div', {'class': 'st_nowosc'}).text.replace('\n', '').strip()]
        except: pass

        # Occasion flag
        try: results += [has_flags.find('div', {'class': 'st_okazja'}).text.replace('\n', '').strip()]
        except: pass

        # Hit prices flag
        try: results += [has_flags.find('div', {'class': 'st_hit_cenowy'}).text.replace('\n', '').strip()]
        except: pass
    return results

def get_links(soup):
    result = []
    for o in soup.find_all('div', {'class': 'single-product'}):
        result += ['https://www.brw.pl' + o.find('div', {'class': 'name'}).find('a')['href']]
    return result