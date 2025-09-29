import datetime

import pandas as pd

from src.decorators import log


@log
def get_expenses_by_category(data: pd.DataFrame, category: str, date=datetime.datetime.now()) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца (90 дней)."""

    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    if isinstance(type(date), str):
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
    start_date = date - datetime.timedelta(days=90)
    expenses_by_category = data.loc[
        (data["Дата операции"] >= start_date) & (data["Дата операции"] <= date) & (data["Категория"].isin([category]))
    ]
    return expenses_by_category
