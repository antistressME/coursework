import datetime
import logging

import pandas as pd

from src.external_api import currency_conversion

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def greeting():
    """Возвращает приветсвие в зависимости от текущего времени."""
    logger.info("Оперделение текущего времени.")
    time_now = datetime.datetime.now().time()

    t_4_00 = datetime.datetime.strptime("2000-01-01 04:00:00.000000", "%Y-%m-%d %H:%M:%S.%f").time()
    t_12_00 = datetime.datetime.strptime("2000-01-01 12:00:00.000000", "%Y-%m-%d %H:%M:%S.%f").time()
    t_16_00 = datetime.datetime.strptime("2000-01-01 16:00:00.000000", "%Y-%m-%d %H:%M:%S.%f").time()

    if t_4_00 <= time_now < t_12_00:
        return "Доброе утро!"
    elif t_12_00 <= time_now < t_16_00:
        return "Добрый день!"
    elif t_16_00 <= time_now:
        return "Добрый вечер!"
    return "Доброй ночи!"


def get_column_values(transactions: pd.DataFrame, column_name: str) -> list:
    """Получаем список уникальных значений из столбца."""
    logger.info("Получаем список уникальных значений из столбца.")

    data = transactions.loc[transactions[column_name].notnull()]
    column_values = data[column_name].unique()
    return list(column_values)


def to_rub(transactions: pd.DataFrame) -> pd.DataFrame:
    """Заменяем сумму операции на сумму в рублях и наименования валют в RUB."""
    logger.info("Конвертируем валюту в рубли. ")

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
    logger.info("Получаем раходные операции.")
    pd_expenses = transactions.loc[(transactions["Статус"] == "OK") & (transactions["Сумма операции"] < 0)]
    return pd_expenses


def get_sum_by_categories(transactions: pd.DataFrame) -> dict:
    """Получаем сумму операций по категориям."""
    logger.info("Получаем сумму операций по категориям.")
    categories = get_column_values(transactions, "Категория")
    sum_by_category = {}
    for item in categories:
        transactions_category = transactions.loc[transactions["Категория"].isin([item])]
        amount_by_category = transactions_category["Сумма операции с округлением"].sum()
        sum_by_category[item] = round(float(amount_by_category), 2)
    return sum_by_category


def get_sum_by_card(transactions: pd.DataFrame) -> dict:
    """Получаем сумму расходов по каждой карте."""
    logger.info("Получаем сумму операций по каждой карте.")
    card_numbers = get_column_values(transactions, "Номер карты")
    sum_by_card = {}
    for card in card_numbers:
        card_transactions = transactions.loc[transactions["Номер карты"].isin([card])]
        amount_by_card = card_transactions["Сумма операции с округлением"].sum()
        sum_by_card[card] = round(float(amount_by_card), 2)
    return sum_by_card


def get_month_transactions(transactions: pd.DataFrame, date=datetime.datetime.now()) -> pd.DataFrame:
    """Получаем операции с 1 числа месяца указанной даты до указанной даты."""
    logger.info("Получаем операции с 1 числа.")
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    if type(date) == str:
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    start_date = date.replace(day=1, hour=0, minute=0, second=0)
    transactions_at_period = transactions.loc[
        (transactions["Дата операции"] <= date) & (transactions["Дата операции"] >= start_date)
    ]
    return transactions_at_period


def top_5_payments(transactions: pd.DataFrame) -> pd.DataFrame:
    """Получаем топ-5 транзакций по сумме платежа."""
    logger.info("Получаем топ-5 транзакций по сумме платежа.")
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


def convert_to_list(transactions: pd.DataFrame) -> list[dict]:
    """Переводит датафрейм в список словарей."""
    logger.info("Получаем список словарей.")
    xlsx_dict = transactions.to_dict("index")
    xlsx_list = []
    for value in xlsx_dict.values():
        xlsx_list.append(dict(value))
    return xlsx_list
