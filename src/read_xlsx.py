import pathlib as Path

import pandas as pd

from src.main import BASEDIR


def get_operations_from_xlsx(path_to_file: str) -> any:
    """Получаем список транзакций из файла Excel"""
    xlsx_data = pd.read_excel(path_to_file)
    return xlsx_data
    # xlsx_dict = xlsx_data.to_dict("index")
    # xlsx_list = []
    # for value in xlsx_dict.values():
    #     xlsx_list.append(dict(value))
    # return xlsx_list


if __name__ == "__main__":
    path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")
    print(get_operations_from_xlsx(path_to_file))
