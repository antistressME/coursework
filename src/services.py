import datetime
import json
import logging
import pathlib as Path

import pandas as pd

from src.read_xlsx import get_operations_from_xlsx
from src.utils import get_expense, get_month_transactions, get_sum_by_categories

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def get_cashback_categories(data: pd.DataFrame, year: int, month: int) -> dict:
    """Получаем словарь выгодных категории для повышенного кешбэка."""
    logger.info("Получаем выгодные категории для повышенного кешбэка.")
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
    return json.dumps(dict(cashback_sum_by_categories), ensure_ascii=False, indent=4)


def search_by_phone_numbers(data: pd.DataFrame) -> pd.DataFrame:
    """Поиск по телефонным номерам."""
    logger.info("Осуществляется поиск по телефонным номерам.")
    xlsx_dict = data.to_dict("index")
    xlsx_list = []
    for value in xlsx_dict.values():
        if "+7" in value["Описание"]:
            xlsx_list.append(dict(value))
    result = pd.DataFrame(xlsx_list)
    return result.to_json(orient="records", force_ascii=False)


if __name__ == "__main__":
    from src.main import BASEDIR

    path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")
    transactions = get_operations_from_xlsx(path_to_file)
    print(search_by_phone_numbers(transactions))
