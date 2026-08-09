import logging
from pathlib import Path

# Настройка логгера
LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "masks.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Обработчик файла (перезаписывается при каждом запуске)
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Формат: время, модуль, уровень, сообщение
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Формат:
        XXXX XX** **** XXXX

    Пример:
        '7000792289606361' -> '7000 79** **** 6361'
    """
    digits_only = card_number.replace(" ", "")
    # Ожидаем, что длина карты >= 10, иначе просто вернем как есть
    if len(digits_only) < 10:
        return card_number

    # Первые 6 и последние 4 цифры
    first_4 = digits_only[:4]  # XXXX
    next_2 = digits_only[4:6]  # XX
    last_4 = digits_only[-4:]  # XXXX

    # Формат строго по заданию: XXXX XX** **** XXXX
    return f"{first_4} {next_2}** **** {last_4}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Формат:
        **XXXX

    Пример:
        '73654108430135874305' -> '**4305'
    """
    digits_only = account_number.replace(" ", "")
    if len(digits_only) <= 4:
        return account_number

    last_4 = digits_only[-4:]
    return f"**{last_4}"
