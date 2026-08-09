from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

from .processing import (
    filter_by_state,
    process_bank_operations,
    process_bank_search,
    sort_by_date,
)
from .transactions import read_transactions_csv, read_transactions_excel
from .utils import load_transactions
from .widget import mask_account_card

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

JSON_FILE = DATA_DIR / "operations.json"
CSV_FILE = DATA_DIR / "transactions.csv"
XLSX_FILE = DATA_DIR / "transactions_excel.xlsx"

Operation = dict[str, Any]

VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def normalize_operation(operation: Mapping[Any, Any]) -> Operation:
    """
    Приводит операцию из JSON, CSV или XLSX к единому формату.
    """
    normalized: Operation = {str(key): value for key, value in operation.items()}

    operation_amount = normalized.get("operationAmount")

    if isinstance(operation_amount, Mapping):
        normalized["amount"] = operation_amount.get("amount")

        currency = operation_amount.get("currency")

        if isinstance(currency, Mapping):
            normalized["currency_name"] = currency.get("name")
            normalized["currency_code"] = currency.get("code")

    for field in ("state", "date", "description", "from", "to"):
        if not isinstance(normalized.get(field), str):
            normalized[field] = ""

    return normalized


def load_operations(source: str) -> list[Operation]:
    """
    Загружает операции из выбранного источника.

    source:
        "1" — JSON;
        "2" — CSV;
        "3" — XLSX.
    """
    raw_operations: Sequence[Mapping[Any, Any]]

    if source == "1":
        raw_operations = load_transactions(str(JSON_FILE))
    elif source == "2":
        raw_operations = read_transactions_csv(CSV_FILE)
    elif source == "3":
        raw_operations = read_transactions_excel(XLSX_FILE)
    else:
        raise ValueError(f"Неизвестный источник данных: {source}")

    return [normalize_operation(operation) for operation in raw_operations]


def normalize_status(status: str) -> str:
    """
    Нормализует и проверяет статус операции.
    """
    normalized_status = status.strip().upper()

    if normalized_status not in VALID_STATUSES:
        allowed_statuses = ", ".join(sorted(VALID_STATUSES))
        raise ValueError(f"Статус операции «{status}» недоступен. " f"Допустимые значения: {allowed_statuses}")

    return normalized_status


def filter_operations_by_status(
    operations: list[Operation],
    status: str,
) -> list[Operation]:
    """
    Фильтрует операции по статусу без учёта регистра.
    """
    normalized_status = normalize_status(status)
    return filter_by_state(operations, normalized_status)


def filter_rub_operations(
    operations: list[Operation],
) -> list[Operation]:
    """
    Возвращает только операции в рублях.
    """
    return [operation for operation in operations if operation.get("currency_code") == "RUB"]


def sort_operations_by_date(
    operations: list[Operation],
    reverse: bool = True,
) -> list[Operation]:
    """
    Сортирует операции по дате и пропускает некорректные даты.
    """
    valid_operations: list[Operation] = []

    for operation in operations:
        raw_date = operation.get("date")

        if not isinstance(raw_date, str) or not raw_date:
            continue

        try:
            datetime.fromisoformat(raw_date)
        except ValueError:
            continue

        valid_operations.append(operation)

    return sort_by_date(valid_operations, reverse=reverse)


def parse_yes_no(answer: str) -> bool:
    """
    Преобразует ответ пользователя в True или False.
    """
    normalized_answer = answer.strip().lower()

    if normalized_answer in {"да", "д", "yes", "y"}:
        return True

    if normalized_answer in {"нет", "н", "no", "n"}:
        return False

    raise ValueError("Введите «да» или «нет».")


def parse_sort_direction(answer: str) -> bool:
    """
    Возвращает направление сортировки.

    True — по убыванию.
    False — по возрастанию.
    """
    normalized_answer = answer.strip().lower()

    if normalized_answer in {
        "по убыванию",
        "убывание",
        "убыванию",
        "desc",
        "2",
    }:
        return True

    if normalized_answer in {
        "по возрастанию",
        "возрастание",
        "возрастанию",
        "asc",
        "1",
    }:
        return False

    raise ValueError("Введите «по возрастанию» или «по убыванию».")


def search_operations(
    operations: list[Operation],
    query: str,
) -> list[Operation]:
    """
    Ищет операции по описанию через регулярное выражение.
    """
    normalized_query = query.strip()

    if not normalized_query:
        return operations

    return process_bank_search(
        operations,
        normalized_query,
    )


def count_operations_by_category(
    operations: list[Operation],
    categories: list[str],
) -> dict[str, int]:
    """
    Подсчитывает количество операций по категориям.
    """
    return process_bank_operations(
        operations,
        categories,
    )


def format_operation(operation: Operation) -> str:
    """
    Форматирует операцию для вывода пользователю.
    """
    raw_date = str(operation.get("date", ""))
    date = raw_date[:10]

    description = str(operation.get("description", ""))
    amount = operation.get("amount", "")
    currency = operation.get("currency_name") or operation.get(
        "currency_code",
        "",
    )

    sender_value = operation.get("from")
    recipient_value = operation.get("to")

    sender = mask_account_card(str(sender_value)) if sender_value else ""
    recipient = mask_account_card(str(recipient_value)) if recipient_value else ""

    result = f"{date}\n{description}\n"

    if sender and recipient:
        result += f"{sender} -> {recipient}\n"
    elif recipient:
        result += f"{recipient}\n"
    elif sender:
        result += f"{sender}\n"

    result += f"Сумма: {amount} {currency}"

    return result


def main() -> None:
    """
    Запускает основную логику приложения.
    """
    print("Привет! Добро пожаловать в программу " "работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию из JSON-файла")
    print("2. Получить информацию из CSV-файла")
    print("3. Получить информацию из XLSX-файла")

    source = input("Ваш выбор: ").strip()

    try:
        operations = load_operations(source)
    except (OSError, ValueError, TypeError) as error:
        print(f"Не удалось загрузить операции: {error}")
        return

    print("Для обработки выбран файл.")
    print(f"Загружено операций: {len(operations)}")

    while True:
        print("\nВведите статус, по которому необходимо " "выполнить фильтрацию.")
        print("Доступные статусы: " "EXECUTED, CANCELED, PENDING")

        status_input = input("Статус: ").strip()

        try:
            operations = filter_operations_by_status(
                operations,
                status_input,
            )
            print(f"Операции отфильтрованы по статусу " f'"{status_input.upper()}"')
            break
        except ValueError as error:
            print(error)

    try:
        should_sort = parse_yes_no(
            input(
                "\nОтсортировать операции по дате? " "Да/Нет: ",
            ),
        )
    except ValueError as error:
        print(error)
        return

    if should_sort:
        while True:
            direction = input(
                "Отсортировать по возрастанию " "или по убыванию? ",
            )

            try:
                reverse = parse_sort_direction(direction)
                operations = sort_operations_by_date(
                    operations,
                    reverse=reverse,
                )
                break
            except ValueError as error:
                print(error)

    try:
        use_rub_only = parse_yes_no(
            input(
                "Выводить только рублёвые транзакции? " "Да/Нет: ",
            ),
        )
    except ValueError as error:
        print(error)
        return

    if use_rub_only:
        operations = filter_rub_operations(operations)

    try:
        use_search = parse_yes_no(
            input(
                "Отфильтровать список транзакций " "по слову в описании? Да/Нет: ",
            ),
        )
    except ValueError as error:
        print(error)
        return

    if use_search:
        query = input(
            "Введите слово или регулярное выражение для поиска: ",
        )
        operations = search_operations(operations, query)

    print("\nРаспечатываю итоговый список транзакций...")

    if not operations:
        print("Не найдено ни одной транзакции, " "подходящей под ваши условия фильтрации.")
        return

    print(f"\nВсего банковских операций в выборке: " f"{len(operations)}\n")

    for operation in operations:
        print(format_operation(operation))
        print()


if __name__ == "__main__":
    main()
