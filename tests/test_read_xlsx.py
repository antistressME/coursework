from unittest.mock import patch

import pandas as pd

from src.read_xlsx import get_operations_from_xlsx


@patch("src.read_xlsx.pd.read_excel")
def test_get_operations_from_xlsx(mock_data_xlsx):
    mock_data_xlsx.return_value = pd.DataFrame({"Yes": [50, 21], "No": [131, 2]})
    assert get_operations_from_xlsx("123") == [{"No": 131, "Yes": 50}, {"No": 2, "Yes": 21}]
    mock_data_xlsx.assert_called()
    mock_data_xlsx.assert_called_once()
