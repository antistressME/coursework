from unittest.mock import Mock, patch

import pandas as pd

from src.read_xlsx import get_operations_from_xlsx


@patch("src.read_xlsx.pd.read_excel")
def test_get_operations_from_xlsx(mock_read_excel):

    mock_df = Mock(spec=pd.DataFrame)
    mock_read_excel.return_value = mock_df
    result = get_operations_from_xlsx("path_to_file")

    mock_read_excel.assert_called_once_with("path_to_file")
    assert result == mock_df


def test_get_operations_from_xlsx_error():
    assert str(get_operations_from_xlsx("wrong_path")) == "Неверный путь к файлу"
