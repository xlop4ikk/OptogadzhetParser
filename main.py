# -------------------------------------------------------------------------
# Парсер товаров с Ozon
# -------------------------------------------------------------------------

from bs4 import BeautifulSoup as BS
import requests

def parsing():
    url = 'https://optogadzhet.ru/product-category/apple/iphone/'
    response = requests.get(url)
    html_content = response.text
    soup = BS(html_content, 'html.parser')
    divs = soup.find_all('div', class_='card-item__main')
    for div in divs:
        links = div.find_all('a')
        for link in links:
            href = link.get('href')
            print(href)
    #print(soup)

parsing()