import re
from collections import Counter
from datetime import datetime
from typing import Any

Operation = dict[str, Any]


def filter_by_state(
    operations: list[Operation],
    state: str,
) -> list[Operation]:
    """
    Фильтрует операции по статусу.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(
    operations: list[Operation],
    reverse: bool = True,
) -> list[Operation]:
    """
    Сортирует операции по дате.
    """

    def parse_date(operation: Operation) -> datetime:
        raw_date = operation.get("date")

        if not isinstance(raw_date, str):
            raise ValueError("Operation date must be a string")

        return datetime.fromisoformat(raw_date)

    return sorted(
        operations,
        key=parse_date,
        reverse=reverse,
    )


def process_bank_search(
    data: list[Operation],
    search: str,
) -> list[Operation]:
    """
    Ищет операции по описанию с помощью регулярного выражения.
    """
    pattern = re.compile(search, re.IGNORECASE)

    return [
        operation
        for operation in data
        if pattern.search(
            str(operation.get("description", "")),
        )
    ]


def process_bank_operations(
    data: list[Operation],
    categories: list[str],
) -> dict[str, int]:
    """
    Подсчитывает количество операций по категориям
    с использованием Counter.
    """
    descriptions = [str(operation.get("description", "")).casefold() for operation in data]

    description_counter = Counter(descriptions)

    return {
        category: description_counter.get(
            category.casefold(),
            0,
        )
        for category in categories
    }
