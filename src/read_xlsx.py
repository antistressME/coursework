import pathlib as Path

import pandas as pd


def get_operations_from_xlsx(path_to_file: str) -> pd.DataFrame:
    """Получаем список транзакций из файла Excel."""
    try:
        xlsx_data = pd.read_excel(path_to_file)
        return xlsx_data
    except:
        return FileNotFoundError("Неверный путь к файлу")


if __name__ == "__main__":
    from src.main import BASEDIR

    path_to_file = Path.Path(BASEDIR / "data" / "operations.xlsx")
    print(get_operations_from_xlsx(path_to_file))
