# -------------------------------------------------------------------------
# Парсер товаров с Optogadzhet
# -------------------------------------------------------------------------

import requests
import csv
from bs4 import BeautifulSoup as BS
from tkinter import *

headers = ['Наименование', 'Ссылка', 'Цена']
root = Tk()
root.title("OptogadzhetParser")
root.geometry("200x220")
root.resizable(False, False)
root.configure(bg="white")
label_name_of_product = Label(root, text="Введите наименование товара:", bg="white", fg="black", font=("Consolas", 10))
texbox_name_of_product = Entry(root, width=25)
label = Label(root, text="Введите номер страницы:", bg="white", fg="black", font=("Consolas", 10))
texbox = Entry(root, width=25)

# -------------------------------------------------------------------------
# Дополнительная форма, выводимая при успешном парсинге
# -------------------------------------------------------------------------
def open_success_form():
    success_window = Toplevel(root)
    success_window.title("Успех")
    success_label = Label(success_window, text="Программа выполнена успешно!")
    success_label.pack()

# -------------------------------------------------------------------------
# Дополнительная форма, выводимая при безуспешном парсинге
# -------------------------------------------------------------------------
def open_error_form():
    error_window = Toplevel(root)
    error_window.title("Ошибка")
    error_label = Label(error_window, text="Произошла ошибка в программе.")
    error_label.pack()

# -------------------------------------------------------------------------
# Основной метод для парсинга сайта
# -------------------------------------------------------------------------
def parsing():
    lst_titles = []
    lst_links = []
    lst_prices = []
    try:
        number_of_page = int(texbox.get())
        open_success_form()
    except:
        open_error_form()
    name_of_product = texbox_name_of_product.get()
    url = f'https://optogadzhet.ru/?page={number_of_page}&s={name_of_product}&post_type=product&dgwt_wcas=1'
    response = requests.get(url)
    html_content = response.text
    soup = BS(html_content, 'html.parser')
    
    # -------------------------------------------------------------------------
    # Парсинг наименований товаров
    # -------------------------------------------------------------------------
    titles = soup.find_all('h3', class_='card-item__title')
    for title in titles:
        lst_titles.append(title.text.strip())

    # -------------------------------------------------------------------------
    # Парсинг ссылок на товары
    # -------------------------------------------------------------------------
    links = soup.find_all('a', class_='card-item__link')
    for link in links:
        lst_links.append(link.get('href'))

    # -------------------------------------------------------------------------
    # Парсинг цен на товары
    # -------------------------------------------------------------------------
    prices = soup.find_all('span', class_='woocommerce-Price-amount amount')
    for price in prices:
        lst_prices.append(price.text.strip())
    modified_list = [item.replace('\xa0₽', '') for item in lst_prices]
    final_list = [item.replace(' ', '') for item in modified_list]
    lst_prices_final = [int(item) for item in final_list] 
    lst_prices_final.pop(0)
    
    # -------------------------------------------------------------------------
    # Создание .csv файла и последующая запись данных
    # -------------------------------------------------------------------------
    with open(f'{name_of_product}_{number_of_page}.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(headers)
        for data in zip(lst_titles, lst_links, lst_prices_final):
            writer.writerow(data)

button = Button(root, text="Начать парсинг!", width=20, height=3, command=parsing)
label_name_of_product.pack(ipadx=20, ipady=8, pady=5, side= "top")
texbox_name_of_product.pack(ipadx=20, ipady=0, pady=5, side= "top")
label.pack(ipadx=20, ipady=8, pady=5, side= "top")
texbox.pack(ipadx=20, ipady=0, pady=5, side= "top")
button.pack(ipadx=20, ipady=8, pady=5, side= "top")
root.mainloop()