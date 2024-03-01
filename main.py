# -------------------------------------------------------------------------
# Парсер товаров с Ozon
# -------------------------------------------------------------------------

from bs4 import BeautifulSoup as BS
import requests

lst_titles = []
lst_links = []
lst_prices = []

def parsing():
    url = 'https://optogadzhet.ru/product-category/apple/iphone/'
    response = requests.get(url)
    html_content = response.text
    soup = BS(html_content, 'html.parser')
    
    print('Названия:')
    titles = soup.find_all('h3', class_='card-item__title')
    for title in titles:
        lst_titles.append(title.text.strip())
    #print(lst_titles)

    print('Ссылки:')
    links = soup.find_all('a', class_='card-item__link')
    for link in links:
        lst_links.append(link.get("href"))
    #print(lst_links)
    
    print('Цены:')
    prices = soup.find_all('span', class_='woocommerce-Price-amount amount')
    for price in prices:
        lst_prices.append(price.text.strip())
    modified_list = [item.replace('\xa0₽', '') for item in lst_prices]
    final_list = [item.replace(' ', '') for item in modified_list]
    lst_prices_final = [int(item) for item in final_list] 
    lst_prices_final.pop(0)
    #print(lst_prices_final)
    
    print(len(lst_titles))
    print(len(lst_links))
    print(len(lst_prices_final))

parsing()