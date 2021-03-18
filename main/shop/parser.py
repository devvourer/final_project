from bs4 import BeautifulSoup as bs
import requests

URL_ROOT = 'https://enter.kg/monitory_bishkek'


def get_html(url):
    respons = requests.get(url)

    return respons.text


def get_page_data(html):
    soup = bs(html, 'html.parser')
    body = soup.find_all('div', class_='row')
    data = []
    for i in body:
        title = i.find('div', class_='product').find('div', class_='rows').text
        price = i.find('div', class_='product').find('span', class_='price').text
        image = i.find('img').get('src')
        product = [title, price.split(' ')[0], 'https://enter.kg/' + image]
        data.append(product)

    return data



