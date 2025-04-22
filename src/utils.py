import datetime
import pathlib as Path

import pandas as pd

from src.main import BASEDIR
from src.read_xlsx import get_operations_from_xlsx

path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")


def get_expense(transactions: pd.DataFrame) -> pd.DataFrame:
    """Получаем раходные операции"""
    pd_expenses = transactions.loc[(transactions["Статус"] == "OK") & (transactions["Сумма операции"] < 0)]
    return pd_expenses


def get_column_values(transactions: pd.DataFrame, column_name: str) -> list:
    """Получаем список уникальных значений из столбца"""
    data = transactions.loc[transactions[column_name].notnull()]
    column_values = data[column_name].unique()
    return list(column_values)


def get_sum_by_categories(transactions: pd.DataFrame) -> dict:
    """Получаем сумму операций по категориям"""
    categories = get_column_values(transactions, "Категория")
    sum_by_category = {}
    for item in categories:
        transactions_category = transactions.loc[transactions["Категория"].isin([item])]
        amount_by_category = transactions_category["Сумма операции с округлением"].sum()
        sum_by_category[item] = float(amount_by_category)
    return sum_by_category


def get_sum_by_card(transactions: pd.DataFrame) -> dict:
    """Получаем сумму расходов по каждой карте"""
    card_numbers = get_column_values(transactions, "Номер карты")
    sum_by_card = {}
    for card in card_numbers:
        card_transactions = transactions.loc[transactions["Номер карты"].isin([card])]
        amount_by_card = card_transactions["Сумма операции с округлением"].sum()
        sum_by_card[card] = float(amount_by_card)
    return sum_by_card


def get_month_transactions(transactions: pd.DataFrame, date=datetime.datetime.now()) -> pd.DataFrame:
    """Получаем операции с 1 числа месяца указанной даты до указанной даты"""
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    month_start = date.replace(day=1, hour=0, minute=0, second=0)
    str_start_date = month_start.strftime("%d.%m.%Y")
    str_end_date = date.strftime("%d.%m.%Y")
    transactions_at_period = transactions.loc[
        (transactions["Дата операции"] >= str_start_date) & (transactions["Дата операции"] <= str_end_date)
    ]
    return transactions_at_period


if __name__ == "__main__":
    transactions = get_operations_from_xlsx(path_to_file)
    print(get_expense(transactions))

    data = get_expense(transactions)
    print(get_sum_by_categories(data))

    print(get_sum_by_card(data))

    date = datetime.datetime(month=1, day=5, year=2018)
    print(get_month_transactions(transactions, date))
