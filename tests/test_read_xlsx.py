from unittest.mock import Mock, patch

import pandas as pd

from src.read_xlsx import get_operations_from_xlsx


@patch("src.read_xlsx.pd.read_excel")
def test_get_operations_from_xlsx(mock_data_xlsx):
    pdata = Mock(spec=pd.DataFrame())
    mock_data_xlsx.return_value = pdata
    assert get_operations_from_xlsx("") == pdata
    mock_data_xlsx.assert_called()
    mock_data_xlsx.assert_called_once()
