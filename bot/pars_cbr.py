import requests
from bs4 import BeautifulSoup


def usd_price() -> str:
    url = 'https://cbr.ru/scripts/XML_daily.asp'

    source = requests.get(url)
    main_text = source.text
    soup = BeautifulSoup(main_text, features="html.parser")

    valute = soup.find_all('valute')
    row = str(valute[10])
    price = row.split('>')[-3].replace('</value', '')
    return f'Курс доллара ЦБ:\n{price}'








