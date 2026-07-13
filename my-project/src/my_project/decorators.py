# my-project/src/my_project/decorators.py

from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования выполнения функций.

    Если filename указан, пишет логи в файл.
    Если filename не указан, выводит логи в консоль.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            function_name = func.__name__

            try:
                result = func(*args, **kwargs)
                message = f"{function_name} ok"
                _write_log(message, filename)
                return result
            except Exception as error:
                error_type = type(error).__name__
                message = (
                    f"{function_name} error: {error_type}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(message, filename)
                # пробрасываем ошибку дальше, чтобы поведение функции не менялось
                raise

        return wrapper

    return decorator


def _write_log(message: str, filename: Optional[str]) -> None:
    """Записать лог либо в файл, либо в консоль."""
    if filename:
        # добавляем строку в файл, не перезаписывая его
        with open(filename, "a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")
    else:
        print(message)
