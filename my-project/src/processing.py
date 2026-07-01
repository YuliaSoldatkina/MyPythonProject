from typing import List, Dict


def filter_by_state(items: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Возвращает список словарей, у которых ключ 'state' равен указанному значению.
    :param items: исходный список словарей
    :param state: нужное значение ключа 'state' (по умолчанию 'EXECUTED')
    """
    return [item for item in items if item.get("state") == state]


def sort_by_date(items: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Возвращает новый список словарей, отсортированный по ключу 'date'.
    :param items: исходный список словарей
    :param reverse: порядок сортировки (по умолчанию True — по убыванию)
    """
    return sorted(items, key=lambda item: item["date"], reverse=reverse)