import requests
import json
from config import keys


class ConvertException(Exception):
    pass

class Convert:
    @staticmethod
    def get_price(currency_start: str, currency_end: str, value: str):
        if currency_start == currency_end:
            raise ConvertException("Невозможно перевести одинаковые валюты")

        try:
            value = float(value)
        except ValueError:
            raise ConvertException(f"Неправильно введено количество валюты - '{value}'")

        if float(value) <= 0:
            raise ConvertException("При конвертации количество валюты должно быть положительным")

        try:
            cheak_currency_start = keys[currency_start]
        except KeyError:
            raise ConvertException(f"Такой валюты нет в нашем списке - '{currency_start}'")

        try:
            cheak_currency_end = keys[currency_end]
        except KeyError:
            raise ConvertException(f"Такой валюты нет в нашем списке - '{currency_end}'")

        r = requests.get(f"https://v6.exchangerate-api.com/v6/bb563a937eda6bf57bfb946f/latest/{cheak_currency_start}")
        ratio = json.loads(r.content)["conversion_rates"][cheak_currency_end]
        return ratio