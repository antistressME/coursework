import datetime
import pathlib as Path

import pandas as pd

from read_xlsx import get_operations_from_xlsx
from src.main import BASEDIR


def get_expenses_by_category(data: pd.DataFrame, category: str, date=datetime.datetime.now()) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца (90 дней)."""

    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    if type(date) == str:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
    start_date = date - datetime.timedelta(days=90)
    expenses_by_category = data.loc[
        (data["Дата операции"] >= start_date) & (data["Дата операции"] <= date) & (data["Категория"].isin([category]))
    ]
    return expenses_by_category


if __name__ == "__main__":
    path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")
    transactions = get_operations_from_xlsx(path_to_file)
    result = get_expenses_by_category(transactions, "Наличные", "20.02.2018")
    xlsx_dict = result.to_dict("index")
    xlsx_list = []
    for value in xlsx_dict.values():
        xlsx_list.append(dict(value))
    print(xlsx_list)
