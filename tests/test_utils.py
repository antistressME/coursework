from unittest.mock import Mock, patch

import pandas as pd

from src.utils import get_card_numbers, get_expense


def test_get_expense(transactions_for_test, expense_for_test):
    pass
    # pdata = Mock(spec=pd.DataFrame(transactions_for_test))
    # assert get_expense(pdata) == expense_for_test


def test_get_card_numbers():
    pass
