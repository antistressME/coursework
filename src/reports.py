import csv
import datetime
import pathlib as Path

import pandas as pd

from read_xlsx import get_operations_from_xlsx
from src.main import BASEDIR


def write_data_to_csv(func):
    """Декоратор, записывающий данные в файл."""

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        result_dict = result.to_dict("index")
        fieldnames = list(result.columns)
        path_to_file = Path.Path(BASEDIR / "data" / "reports.csv")
        with open(path_to_file, "w") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for value in result_dict.values():
                writer.writerow(value)

    return inner


@write_data_to_csv
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
