# my-project/src/my_project/widget.py

from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(raw_data: str) -> str:

    # Разделяем по последнему пробелу: слева имя, справа номер
    name, number = raw_data.rsplit(" ", 1)

    # Если это счёт
    if name.startswith("Счет"):
        masked = get_mask_account(number)
        return f"{name} {masked}"

    # Иначе считаем, что это карта
    masked = get_mask_card_number(number)
    return f"{name} {masked}"


def get_date(raw_date: str) -> str:

    dt = datetime.fromisoformat(raw_date)
    return dt.strftime("%d.%m.%Y")
