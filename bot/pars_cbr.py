import requests
from bs4 import BeautifulSoup as bs


def usd_price() -> str:
    url = 'https://cbr.ru/scripts/XML_daily.asp'

    get_html = requests.get(url)
    if get_html.status_code == 200:
        soup = bs(get_html.content, 'html.parser')
        rate = soup.find('valute', attrs={'id': 'R01235'}).find('value').text
        return f'Курс доллара ЦБ:\n{rate}'








