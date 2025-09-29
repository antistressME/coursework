import datetime

import pandas as pd

from src.utils import get_expense, get_month_transactions, get_sum_by_categories


def get_cashback_categories(data: pd.DataFrame, year: int, month: int) -> dict:
    """Получаем словарь выгодных категории для повышенного кешбэка."""

    if month == 12:
        date_str = f"01.01.{year + 1} 23:59:59"
    else:
        date_str = f"01.{month + 1}.{year} 23:59:59"
    date_object = datetime.datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
    date = date_object - datetime.timedelta(days=1)
    month_transactions = get_month_transactions(data, date)
    expenses = get_expense(month_transactions)
    sum_by_categories = get_sum_by_categories(expenses)
    for key, value in sum_by_categories.items():
        if key in ["Наличные", "Переводы"]:
            sum_by_categories[key] = 0
        else:
            sum_by_categories[key] = int(value // 100)
    cashback_sum_by_categories = sorted(sum_by_categories.items(), key=lambda item: item[1], reverse=True)
    return dict(cashback_sum_by_categories)


def search_by_phone_numbers(data: pd.DataFrame) -> pd.DataFrame:
    """Поиск по телефонным номерам."""
    xlsx_dict = data.to_dict("index")
    xlsx_list = []
    for value in xlsx_dict.values():
        if "+7" in value["Описание"]:
            xlsx_list.append(dict(value))
    return pd.DataFrame(xlsx_list)
