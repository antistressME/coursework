import datetime
import pathlib as Path

import pandas as pd

from src.main import BASEDIR
from src.read_xlsx import get_operations_from_xlsx

path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")


def get_expense(transactions):
    """Получаем раходные операции"""
    pd_expenses = transactions.loc[(transactions["Статус"] == "OK") & (transactions["Сумма операции"] < 0)]
    return pd_expenses


if __name__ == "__main__":
    transactions = get_operations_from_xlsx(path_to_file)
    print(get_expense(transactions))


def get_card_numbers(transactions) -> list:
    """Получаем список карт"""
    data = transactions.loc[transactions["Номер карты"].notnull()]
    card_numbers = data["Номер карты"].unique()
    return list(card_numbers)


if __name__ == "__main__":
    transactions = get_operations_from_xlsx(path_to_file)
    print(get_card_numbers(transactions))


def get_categories(transactions) -> list:
    """Получаем список категорий"""
    data = transactions.loc[transactions["Категория"].notnull()]
    categories = data["Категория"].unique()
    return list(categories)


if __name__ == "__main__":
    transactions = get_operations_from_xlsx(path_to_file)
    print(get_categories(transactions))


def get_sum_by_categories(transactions, categories: list) -> dict:
    """Получаем сумму операций по категориям"""
    sum_by_category = {}
    for item in categories:
        transactions_category = transactions.loc[transactions["Категория"].isin([item])]
        amount_by_category = transactions_category["Сумма операции с округлением"].sum()
        sum_by_category[item] = float(amount_by_category)
    return sum_by_category


if __name__ == "__main__":
    transactions = get_operations_from_xlsx(path_to_file)
    data = get_expense(transactions)
    categories = get_categories(transactions)
    print(get_sum_by_categories(data, categories))


def get_sum_by_card(transactions, card_numbers: list) -> dict:
    """Получаем сумму расходов по каждой карте"""
    sum_by_card = {}
    for card in card_numbers:
        card_transactions = transactions.loc[transactions["Номер карты"].isin([card])]
        amount_by_card = card_transactions["Сумма операции с округлением"].sum()
        sum_by_card[card] = float(amount_by_card)
    return sum_by_card


if __name__ == "__main__":
    transactions = get_operations_from_xlsx(path_to_file)
    data = get_expense(transactions)
    card_numbers = get_card_numbers(transactions)
    print(get_sum_by_card(data, card_numbers))


# def get_period(transactions, date=datetime.datetime.now()):
#     """Получаем период времени по указанной дате"""
#     transactions_date = datetime.datetime.strptime(transactions["Дата операции"], "%d.%m.%Y %H:%M:%S")
#     beginning_of_the_month = date.replace(day=1, hour=0, minute=0, second=0)
#     transactions_at_petiod = transactions.loc[(transactions_date > beginning_of_the_month) & (transactions_date < date)]
#     return transactions_at_petiod
#
# if __name__ == '__main__':
#     transactions = get_operations_from_xlsx(path_to_file)
#     print(get_period(transactions))
