"""
Получение курсов валют
"""


from enum import Enum

import requests
from fake_useragent import UserAgent

headers = {
    'user-agent': UserAgent().random,
    'X-Requested-With': 'XMLHttpRequest'
}


class Currencies(str, Enum):
    """Доступные курсы валют"""

    CNY = 'R01375'
    USD = 'R01235'
    EUR = 'R01239'
    BYN = 'R01090B'
    AED = 'R01230'
    SGD = 'R01625'


def get_exchange_rate(currency: Currencies) -> float:
    """
    Получает текущий курс валюты с сайта Центробанка РФ
    
    :param currency: Валюта из перечисления Currencies
    :return: Текущий курс валюты
    """
    url = 'https://cbr.ru/cursonweek'
    params = {'DT': '', 'val_id': currency.value}
    response = requests.get(url, headers=headers, params=params, timeout=10).json()[0]
    return float(response['curs'])


# def get_active_currency_codes() -> list[dict[str, Any]]:
#     url = 'https://www.cbr.ru/scripts/XML_daily.asp'
#     response = requests.get(url)
#     response.encoding = 'windows-1251'

#     root = ET.fromstring(response.text)
#     currencies = []

#     for valute in root.findall('Valute'):
#         currencies.append({
#             'name':
#             valute.find('Name').text,
#             'char_code':
#             valute.find('CharCode').text,
#             'cbr_code':
#             valute.attrib['ID'],
#             'nominal':
#             int(valute.find('Nominal').text),
#             'value':
#             float(valute.find('Value').text.replace(',', '.'))
#         })

#     return currencies
