import datetime
import json
import pathlib as Path

from external_api import get_currencies, get_stocks
from src.main import BASEDIR
from src.read_xlsx import get_operations_from_xlsx
from utils import convert_to_list, get_expense, get_month_transactions, get_sum_by_card, greeting, top_5_payments

path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")


def main_page(date_: str):
    date = datetime.datetime.strptime(date_, "%Y-%m-%d %H:%M:%S")
    transactions = get_operations_from_xlsx(path_to_file)  # читаем файл с операциями
    month_transactions = get_month_transactions(
        transactions, date
    )  # Получаем операции с 1 числа месяца указанной даты до указанной даты
    expenses = get_expense(month_transactions)  # Получаем раходные операции

    sum_by_card = get_sum_by_card(expenses)  # Получаем сумму расходов по каждой карте {"*7197": 478419.56}
    cards = []
    for key, value in sum_by_card.items():
        card = {"last_digits": key[-4:], "total_spent": value, "cashback": round(value / 100, 2)}
        cards.append(card)

    top_transactions = convert_to_list(top_5_payments(expenses))
    top_transactions_list = []
    for item in top_transactions:
        transaction = {
            "date": item["Дата платежа"],
            "amount": item["Сумма операции с округлением"],
            "category": item["Категория"],
            "description": item["Описание"],
        }
        top_transactions_list.append(transaction)

    rate_eur = get_currencies("EUR")
    rate_usd = get_currencies("USD")

    result = {
        "greeting": greeting(),
        "cards": cards,
        "top_transactions": top_transactions_list,
        "currency_rates": [
            {
                "currency": "USD",
                "rate": rate_usd,  # не могу получить курс валют, так как не оформлена платная подписка
            },
            {
                "currency": "EUR",
                "rate": rate_eur,  # не могу получить курс валют, так как не оформлена платная подписка
            },
        ],
        "stock_prices": [
            {"stock": "AAPL", "price": get_stocks("AAPL")},
            {"stock": "AMZN", "price": get_stocks("AMZN")},
            {"stock": "GOOGL", "price": get_stocks("GOOGL")},
        ],
    }
    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(main_page("2018-01-20 10:10:10"))
