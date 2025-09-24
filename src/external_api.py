import json
import os

import requests
from dotenv import load_dotenv


def currency_conversion(amount: float, currency: str) -> float:
    """Переводит сумму в рубли."""
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={"RUB"}&from={currency}&amount={amount}"
    load_dotenv()
    key = os.getenv("API_KEY")
    api_key = {"apikey": key}
    response = requests.request("GET", url, headers=api_key, timeout=9)
    status_code = response.status_code
    if status_code == 200:
        content = json.loads(response.text)
        amount_rub = round(content["result"], 2)
        return amount_rub
    else:
        error_message = f"An error {status_code} occurred. Please try again later."
        print(error_message)


def get_currencies(currency: str) -> dict:
    """Получаем курс валют."""
    key = os.getenv("API_KEY_TWELVEDATA")
    url = f"https://api.twelvedata.com/exchange_rate?symbol={currency}/RUB&apikey={key}"
    response = requests.request("GET", url, headers={"apikey": key}, timeout=9)
    status_code = response.status_code
    if status_code == 200:
        return json.loads(response.text)
    else:
        error_message = f"An error {status_code} occurred. Please try again later."
        print(error_message)


# https://www.alphavantage.co/
# акции
def get_stocks():
    """Получаем акции."""
    key = os.getenv("API_KEY_ALPHAVANTAGE")
    url = f"https://www.alphavantage.co/query?function=REALTIME_OPTIONS&interval=5min&apikey={key}"
    response = requests.request("GET", url, headers={"apikey": key}, timeout=9)
    status_code = response.status_code
    if status_code == 200:
        return json.loads(response.text)
    else:
        error_message = f"An error {status_code} occurred. Please try again later."
        print(error_message)


if __name__ == "__main__":
    print(get_stocks())
