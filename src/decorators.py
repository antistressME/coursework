import csv
import pathlib as Path
from functools import wraps

from src.main import BASEDIR


def log(filename="reports.csv", *args, **kwargs):
    """Декоратор записывает результат работы функции в файл."""

    def wrapper(func, *args, **kwargs):

        @wraps(func)
        def innit(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
            except:
                log_message = f"{func.__name__} error: {Exception.__class__.__name__}. Inputs: {args}, {kwargs}"
            result_dict = result.to_dict("index")
            fieldnames = list(result.columns)
            path_to_file = Path.Path(BASEDIR / "data" / filename)
            with open(path_to_file, "w", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for value in result_dict.values():
                    writer.writerow(value)
            return log_message

        return innit

    return wrapper
