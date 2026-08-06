import os
from pathlib import Path

from src.my_project.transactions import read_transactions_csv, read_transactions_excel


BASE_DIR = Path(os.path.dirname(os.path.dirname(__file__)))


def test_read_transactions_csv_returns_list_of_dicts() -> None:
    file_path = BASE_DIR / "transactions.csv"

    result = read_transactions_csv(file_path)

    assert isinstance(result, list)
    assert len(result) > 0
    first = result[0]
    assert isinstance(first, dict)
    # ожидаемые ключи
    for key in ("id", "state", "date", "amount", "currency_name", "currency_code", "from", "to", "description"):
        assert key in first


def test_read_transactions_excel_returns_list_of_dicts() -> None:
    file_path = BASE_DIR / "transactions_excel.xlsx"

    result = read_transactions_excel(file_path)

    assert isinstance(result, list)
    assert len(result) > 0
    first = result[0]
    assert isinstance(first, dict)
    for key in ("id", "state", "date", "amount", "currency_name", "currency_code", "from", "to", "description"):
        assert key in first
