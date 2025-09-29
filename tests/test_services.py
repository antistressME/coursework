import pandas as pd

from src.services import get_cashback_categories, search_by_phone_numbers


def test_get_cashback_categories(transactions_for_test):
    df = pd.DataFrame(transactions_for_test)
    result = get_cashback_categories(df, 2021, 12)
    assert result == {"Различные товары": 5, "Супермаркеты": 4, "Каршеринг": 0, "Переводы": 0}


def test_search_by_phone_numbers(transactions_for_test_search):
    df = pd.DataFrame(transactions_for_test_search)
    result = search_by_phone_numbers(df)
    assert len(result) == 1
    assert result.to_dict("index")[0]["Описание"] == "Я МТС +7 921 11-22-33"


def test_search_by_phone_numbers_empty(transactions_for_test):
    df = pd.DataFrame(transactions_for_test)
    result = search_by_phone_numbers(df)
    assert len(result) == 0
