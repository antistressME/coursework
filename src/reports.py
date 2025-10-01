import datetime
import logging
import pathlib as Path

import pandas as pd

from src.decorators import log
from src.read_xlsx import get_operations_from_xlsx

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


@log(filename="reports.csv")
def get_expenses_by_category(data: pd.DataFrame, category: str, date=datetime.datetime.now()) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца (90 дней)."""
    logger.info("Оперделение трат по заданной категории за последние три месяца (90 дней).")
    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    if type(date) == str:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
    start_date = date - datetime.timedelta(days=90)
    expenses_by_category = data.loc[
        (data["Дата операции"] >= start_date) & (data["Дата операции"] <= date) & (data["Категория"].isin([category]))
    ]
    return expenses_by_category


if __name__ == "__main__":
    from src.main import BASEDIR

    path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")
    transactions = get_operations_from_xlsx(path_to_file)
    print(get_expenses_by_category(transactions, "Наличные", "20.01.2018"))
