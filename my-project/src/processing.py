def filter_by_state(items: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Возвращает список словарей, у которых ключ 'state' равен указанному значению.
    :param items: исходный список словарей
    :param state: нужное значение ключа 'state' (по умолчанию 'EXECUTED')
    """
    return [item for item in items if item.get("state") == state]