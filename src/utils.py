import datetime
import pathlib as Path

import pandas as pd

from external_api import currency_conversion
from src.main import BASEDIR
from src.read_xlsx import get_operations_from_xlsx

path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")


def greeting(date=datetime.datetime.now()):
    """Возвращает приветсвие в зависимости от текущего времени."""

    time_now = date.time()
    t_4_00 = datetime.datetime.strptime("2000-01-01 04:00:00.000000", "%Y-%m-%d %H:%M:%S.%f").time()
    t_12_00 = datetime.datetime.strptime("2000-01-01 12:00:00.000000", "%Y-%m-%d %H:%M:%S.%f").time()
    t_16_00 = datetime.datetime.strptime("2000-01-01 16:00:00.000000", "%Y-%m-%d %H:%M:%S.%f").time()

    if t_4_00 <= time_now < t_12_00:
        return "Доброе утро!"
    elif t_12_00 <= time_now < t_16_00:
        return "Добрый день!"
    elif t_16_00 < time_now:
        return "Добрый вечер!"
    return "Доброй ночи!"


def get_column_values(transactions: pd.DataFrame, column_name: str) -> list:
    """Получаем список уникальных значений из столбца."""

    data = transactions.loc[transactions[column_name].notnull()]
    column_values = data[column_name].unique()
    return list(column_values)


def to_rub(transactions: pd.DataFrame) -> pd.DataFrame:
    """Заменяем сумму операции на сумму в рублях и наименования валют в RUB."""

    currencies = get_column_values(transactions, "Валюта операции")
    currencies.remove("RUB")
    for currency in currencies:
        transactions.loc[
            transactions["Валюта операции"] == currency, currency_conversion("Сумма операции с округлением", currency)
        ]
        transactions.loc[transactions["Валюта операции"] == currency, "Валюта операции"] = "RUB"
    return transactions


def get_expense(transactions: pd.DataFrame) -> pd.DataFrame:
    """Получаем раходные операции."""
    pd_expenses = transactions.loc[(transactions["Статус"] == "OK") & (transactions["Сумма операции"] < 0)]
    return pd_expenses


def get_sum_by_categories(transactions: pd.DataFrame) -> dict:
    """Получаем сумму операций по категориям."""
    categories = get_column_values(transactions, "Категория")
    sum_by_category = {}
    for item in categories:
        transactions_category = transactions.loc[transactions["Категория"].isin([item])]
        amount_by_category = transactions_category["Сумма операции с округлением"].sum()
        sum_by_category[item] = round(float(amount_by_category), 2)
    return sum_by_category


def get_sum_by_card(transactions: pd.DataFrame) -> dict:
    """Получаем сумму расходов по каждой карте."""
    card_numbers = get_column_values(transactions, "Номер карты")
    sum_by_card = {}
    for card in card_numbers:
        card_transactions = transactions.loc[transactions["Номер карты"].isin([card])]
        amount_by_card = card_transactions["Сумма операции с округлением"].sum()
        sum_by_card[card] = float(amount_by_card)
    return sum_by_card


def get_month_transactions(transactions: pd.DataFrame, date=datetime.datetime.now()) -> pd.DataFrame:
    """Получаем операции с 1 числа месяца указанной даты до указанной даты."""
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    month_start = date.replace(day=1, hour=0, minute=0, second=0)
    str_start_date = month_start.strftime("%d.%m.%Y")
    str_end_date = date.strftime("%d.%m.%Y")
    transactions_at_period = transactions.loc[
        (transactions["Дата операции"] >= str_start_date) & (transactions["Дата операции"] <= str_end_date)
    ]
    return transactions_at_period


def top_5_payments(transactions: pd.DataFrame) -> pd.DataFrame:
    """Получаем топ-5 транзакций по сумме платежа."""

    transactions.sort_values(
        "Сумма операции с округлением",
        axis=0,
        ascending=False,
        inplace=True,
        kind="quicksort",
        na_position="last",
        ignore_index=False,
        key=None,
    )
    return transactions[:5]


if __name__ == "__main__":
    transactions = get_operations_from_xlsx(path_to_file)
    payments = get_expense(transactions)
    # print(top_5_payments(payments))
    # print(get_expense(transactions))
    xlsx_dict = get_expense(transactions).to_dict("index")
    xlsx_list = []
    for value in xlsx_dict.values():
        xlsx_list.append(dict(value))
    for i in xlsx_list:
        print(i["Описание"])  # МТС Mobile +7 981 888-88-88
    #
    # print(get_sum_by_categories(payments))
    #
    # print(get_sum_by_card(data))
    #
    # date = datetime.datetime(month=1, day=5, year=2018)
    # print(get_month_transactions(transactions, date))
    #
    # print(get_column_values(transactions, "Валюта операции"))
