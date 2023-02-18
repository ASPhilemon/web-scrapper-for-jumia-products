import requests
from bs4 import BeautifulSoup
import time
import os

class Products:
    time_delay = 2

    def __init__(self, product_category):
        self.product_category = product_category
        self.product_dict = {}
        self.fetch_products()

    def fetch_products(self):
        print(f'Fetching products for {self.product_category} category', '...')
        product_url = 'https://www.jumia.ug/' + self.product_category
        page = 1
        while True:
            page_url = product_url + f"/?page={page}"
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for line in soup.strings:
                isEnd = 'No results found!' in line
                if isEnd:
                    return
            product_articles = soup.find_all('article')
            for product_article in product_articles:
                try:
                    name = product_article.find(class_='name').text
                    price = product_article.find(class_='prc').text
                    self.product_dict[name] = price
                except:
                    pass
            #Delay between subsequent requests to bypass bot detection
            time.sleep(self.time_delay)
            page = page + 1

    def save_to_disk(self, file_name):
        print(f'Saving products for {self.product_category} category', '...')
        folder = "products"
        isExist = os.path.exists(folder)
        if not isExist:
            os.makedirs(folder)
        file_path = os.getcwd()+ '/products/' + file_name
        with open(file_path, 'w', encoding='utf-8') as fhand:
            for name, price in self.product_dict.items():
                fhand.write(f"{name},{price}\n")

#A sample of product categories
Products('mobile-phones').save_to_disk('mobile_phones.csv')
Products('laptops').save_to_disk('laptops.csv')
Products('electronics').save_to_disk('electronics.csv')
Products('groceries').save_to_disk('groceries.csv')
Products('automobile').save_to_disk('automobile.csv')