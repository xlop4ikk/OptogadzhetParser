# -------------------------------------------------------------------------
# Парсер товаров с Ozon
# -------------------------------------------------------------------------

from bs4 import BeautifulSoup as BS
import requests
import csv
from tkinter import *
import random

lst_titles = []
lst_links = []
lst_prices = []
absolute_links = []
headers = ['Наименование', 'Ссылка', 'Цена']

root = Tk()
root.title("OptogadzhetParser")
root.geometry("200x200")
root.resizable(False, False)
root.configure(bg="white")
success = Label(root, text="Парсинг прошел успешно!")
error = Label(root, text="Такой страницы нет!")

def parsing():
    url = 'https://optogadzhet.ru/product-category/apple/iphone/'
    response = requests.get(url)
    html_content = response.text
    soup = BS(html_content, 'html.parser')
    
    #print('Названия:')
    titles = soup.find_all('h3', class_='card-item__title')
    for title in titles:
        lst_titles.append(title.text.strip())
    #print(lst_titles)

    #print('Ссылки:')
    links = soup.find_all('a', class_='card-item__link')
    for link in links:
        lst_links.append(link.get('href'))
    #print(lst_links)
    
    #print('Цены:')
    prices = soup.find_all('span', class_='woocommerce-Price-amount amount')
    for price in prices:
        lst_prices.append(price.text.strip())
    modified_list = [item.replace('\xa0₽', '') for item in lst_prices]
    final_list = [item.replace(' ', '') for item in modified_list]
    lst_prices_final = [int(item) for item in final_list] 
    lst_prices_final.pop(0)
    #print(lst_prices_final)
    
    #print(len(lst_titles))
    #print(len(lst_links))
    #print(len(lst_prices_final))
    
    """random_number = random.randint(0, 100)
    with open(f'output{random_number}.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(headers)
        for data in zip(lst_titles, lst_links, lst_prices_final):
            writer.writerow(data)"""

#parsing()
label = Label(root, text="Введите номер страницы:", bg="white", fg="black", font=("Consolas", 11))
texbox = Entry(root, width=25)
button = Button(root, text="Начать парсинг!", width=20, height=3, command=parsing)
label.pack(ipadx=20, ipady=8, pady=5, side= "top")
texbox.pack(ipadx=20, ipady=0, pady=5, side= "top")
button.pack(ipadx=20, ipady=8, pady=5, side= "top")
root.mainloop()