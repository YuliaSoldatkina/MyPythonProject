from collections.abc import Hashable
from pathlib import Path
from typing import Any

import pandas as pd


def read_transactions_csv(file_path: str | Path) -> list[dict[Hashable, Any]]:
    """
    Читает транзакции из CSV-файла с разделителем ';'.
    """
    df = pd.read_csv(file_path, sep=";")
    return df.to_dict(orient="records")


def read_transactions_excel(file_path: str | Path) -> list[dict[Hashable, Any]]:
    """
    Читает транзакции из XLSX-файла.
    """
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")
