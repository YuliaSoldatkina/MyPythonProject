from typing import Any, Dict, Iterable, Iterator


def filter_by_currency(
    transactions: Iterable[Dict[str, Any]],
    currency: str,
) -> Iterator[Dict[str, Any]]:
    """
    Генератор, который по очереди выдаёт транзакции
    с указанной валютой, например 'USD'.

    Ожидает формат данных Skypro:
    transaction["operationAmount"]["currency"]["code"] == currency.
    """
    for tx in transactions:
        code = tx.get("operationAmount", {}).get("currency", {}).get("code")
        if code == currency:
            yield tx


def transaction_descriptions(
    transactions: Iterable[Dict[str, Any]],
) -> Iterator[str]:
    """
    Генератор, который по очереди возвращает описание операции.

    Ожидает, что описание лежит по ключу 'description'.
    Если ключа нет, возвращает пустую строку.
    """
    for tx in transactions:
        yield tx.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате 'XXXX XXXX XXXX XXXX',
    где X — цифра номера карты.

    Диапазон от 0000 0000 0000 0001 (start=1)
    до 9999 9999 9999 9999.
    """
    if start < 1:
        start = 1
    max_value = 9_999_999_999_999_999
    if end > max_value:
        end = max_value

    for number in range(start, end + 1):
        raw = f"{number:016d}"  # 16 цифр с ведущими нулями
        yield f"{raw[0:4]} {raw[4:8]} {raw[8:12]} {raw[12:16]}"
