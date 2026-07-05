# src/my_project/processing.py

from datetime import datetime
from typing import List, Dict, Any


def filter_by_state(operations: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по заданному статусу 'state'.

    operations: список операций, каждая операция — словарь,
                например {"state": "EXECUTED", "date": "...", ...}
    state: статус, по которому фильтруем, например "EXECUTED" или "CANCELED".

    Возвращает новый список словарей с операциями, у которых state == заданному.
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по полю 'date'.

    operations: список операций, каждая операция — словарь с ключом 'date'.
    reverse: если True, сортируем по дате в порядке убывания (новые сверху),
             если False — по возрастанию.

    Ожидает дату в ISO-формате, например '2024-03-11T02:26:18.671407'.
    """
    def parse_date(op: Dict[str, Any]) -> datetime:
        raw = op.get("date")
        return datetime.fromisoformat(raw)

    return sorted(operations, key=parse_date, reverse=reverse)
