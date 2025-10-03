import pandas as pd
import pytest
from freezegun import freeze_time

from src.utils import (convert_to_list, get_column_values, get_expense, get_month_transactions, get_sum_by_card,
                       get_sum_by_categories, greeting, top_5_payments)


def test_convert_to_list(transactions_for_test, expense_for_test):
    df = pd.DataFrame(transactions_for_test)
    df_expense = pd.DataFrame(expense_for_test)
    result1 = convert_to_list(df)
    result2 = convert_to_list(df_expense)
    assert type(result1) == list
    assert type(result2) == list
    assert result1.sort(key=lambda dictionary: dictionary["Дата операции"]) == transactions_for_test.sort(
        key=lambda dictionary: dictionary["Дата операции"]
    )
    assert result2.sort(key=lambda dictionary: dictionary["Дата операции"]) == expense_for_test.sort(
        key=lambda dictionary: dictionary["Дата операции"]
    )


def test_get_expense(transactions_for_test, expense_for_test):
    df = pd.DataFrame(transactions_for_test)
    df_expense = pd.DataFrame(expense_for_test)
    result = get_expense(df)
    assert result.shape == df_expense.shape
    assert result["Сумма операции"].sum() == df_expense["Сумма операции"].sum()


test_cases = [
    ("03:59:59", "Доброй ночи!"),
    ("04:00:00", "Доброе утро!"),
    ("11:59:59", "Доброе утро!"),
    ("12:00:00", "Добрый день!"),
    ("15:59:59", "Добрый день!"),
    ("16:00:00", "Добрый вечер!"),
    ("23:59:59", "Добрый вечер!"),
    ("00:00:00", "Доброй ночи!"),
]


@pytest.mark.parametrize("test_time, expected_result", test_cases)
def test_greeting(test_time, expected_result):
    """
    Тестируем функцию приветствия для разных временных интервалов.
    """
    with freeze_time(f"2025-09-25 {test_time}"):
        result = greeting()
        assert result == expected_result, f"Ожидалось {expected_result}, но получено {result}"


def test_edge_cases():
    """
    Тестирование граничных случаев.
    """
    # Проверяем точное совпадение с границами
    with freeze_time("2025-09-25 04:00:00"):
        assert greeting() == "Доброе утро!"

    with freeze_time("2025-09-25 12:00:00"):
        assert greeting() == "Добрый день!"

    with freeze_time("2025-09-25 16:00:00"):
        assert greeting() == "Добрый вечер!"


def test_random_times():
    """
    Тестирование случайных временных точек.
    """
    test_points = [
        ("06:30:00", "Доброе утро!"),
        ("09:45:00", "Доброе утро!"),
        ("13:25:00", "Добрый день!"),
        ("14:15:00", "Добрый день!"),
        ("17:30:00", "Добрый вечер!"),
        ("20:45:00", "Добрый вечер!"),
    ]

    for test_time, expected in test_points:
        with freeze_time(f"2025-09-25 {test_time}"):
            assert greeting() == expected


# Создаем тестовые данные


def test_get_column_values_basic(transactions_for_test):
    df = pd.DataFrame(transactions_for_test)
    result = get_column_values(df, "Номер карты")
    result2 = get_column_values(df, "Описание")
    assert result == ["*7197", "*5091", "*4556"]
    assert result2 == ["Колхоз", "Магнит", "Ozon.ru", "Константин Л.", "Ситидрайв", "Пополнение через Газпромбанк"]


def test_get_column_values_empty_column():
    df = pd.DataFrame({"empty_column": [None, None, None]})
    result = get_column_values(df, "empty_column")
    assert result == []


def test_get_sum_by_categories_basic(transactions_for_test):
    df = pd.DataFrame(transactions_for_test)
    result = get_sum_by_categories(df)
    assert result == {
        "Супермаркеты": 421.06,
        "Различные товары": 564.0,
        "Переводы": 20800.0,
        "Каршеринг": 8.39,
        "Пополнения": 5046.0,
    }


def test_get_sum_by_categories_zero_values():
    df = pd.DataFrame(
        {"Категория": ["Продукты", "Продукты", "Развлечения"], "Сумма операции с округлением": [0.00, 0.00, 0.00]}
    )
    result = get_sum_by_categories(df)
    expected = {"Продукты": 0.00, "Развлечения": 0.00}
    assert result == expected


def test_get_sum_by_categories_negative_values():
    df = pd.DataFrame(
        {"Категория": ["Возврат", "Возврат", "Покупка"], "Сумма операции с округлением": [-100.00, -50.00, 200.00]}
    )
    result = get_sum_by_categories(df)
    expected = {"Возврат": -150.00, "Покупка": 200.00}
    assert result == expected


def test_get_sum_by_card_basic(transactions_for_test):
    df = pd.DataFrame(transactions_for_test)
    result = get_sum_by_card(df)
    assert result == {"*7197": 422.38, "*5091": 571.07, "*4556": 5046.0}


def test_get_sum_by_card_zero_values():
    df = pd.DataFrame(
        {
            "Номер карты": ["4111111111111111", "4111111111111111", "5555555555555555"],
            "Сумма операции с округлением": [0.00, 0.00, 0.00],
        }
    )
    result = get_sum_by_card(df)
    expected = {"4111111111111111": 0.00, "5555555555555555": 0.00}
    assert result == expected


def test_get_sum_by_card_missing_card():
    df = pd.DataFrame(
        {
            "Номер карты": ["4111111111111111", None, "5555555555555555"],
            "Сумма операции с округлением": [100.00, 200.00, 300.00],
        }
    )
    result = get_sum_by_card(df)
    expected = {"4111111111111111": 100.00, "5555555555555555": 300.00}
    assert result == expected


def test_get_month_transactions(transactions_for_test):
    df = pd.DataFrame(transactions_for_test)
    result = get_month_transactions(df, "30.12.2021 19:06:39")
    assert result.shape == (2, 15)
    assert result["Сумма операции"].sum() == 5044.68


def test_top_5_payments(transactions_for_test):
    df = pd.DataFrame(transactions_for_test)
    result = top_5_payments(df)
    assert len(result) == 5
    assert list(result["Сумма операции с округлением"]) == [20000.0, 5046.0, 800.0, 564.0, 160.89]
