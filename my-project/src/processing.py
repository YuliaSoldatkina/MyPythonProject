from typing import Dict, List


def filter_by_state(items: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Фильтрует операции по значению ключа 'state'.
    """
    return [item for item in items if item.get("state") == state]


def sort_by_date(items: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Возвращает новый список словарей, отсортированный по ключу 'date'.
    """
    return sorted(items, key=lambda item: item["date"], reverse=reverse)
