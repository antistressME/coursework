import datetime
import pathlib as Path

import pandas as pd

from read_xlsx import get_operations_from_xlsx
from src.main import BASEDIR
from utils import get_column_values, get_expense, get_month_transactions, get_sum_by_categories


def get_cashback_categories(data: pd.DataFrame, year: int, month: int) -> dict:
    """Получаем словарь выгодных категории для повышенного кешбэка."""

    date_str = f"01.{month + 1}.{year}"
    date_object = datetime.datetime.strptime(date_str, "%d.%m.%Y")
    date = date_object - datetime.timedelta(days=1)
    month_transactions = get_month_transactions(data, date)
    expenses = get_expense(month_transactions)
    sum_by_categories = get_sum_by_categories(expenses)
    del sum_by_categories["Наличные"]
    del sum_by_categories["Переводы"]
    for key, value in sum_by_categories.items():
        sum_by_categories[key] = int(value // 100)
    cashback_sum_by_categories = sorted(sum_by_categories.items(), key=lambda item: item[1], reverse=True)
    return dict(cashback_sum_by_categories)


def search_by_phone_numbers(data: pd.DataFrame) -> pd.DataFrame:
    """Поиск по телефонным номерам."""
    xlsx_dict = data.to_dict("index")
    xlsx_list = []
    for value in xlsx_dict.values():
        if " +7 " in value["Описание"]:
            xlsx_list.append(dict(value))
    return pd.DataFrame(xlsx_list)


if __name__ == "__main__":
    path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")

    transactions = get_operations_from_xlsx(path_to_file)
    # print(get_cashback_categories(transactions, 2018, 8))
    print(search_by_phone_numbers(transactions))
