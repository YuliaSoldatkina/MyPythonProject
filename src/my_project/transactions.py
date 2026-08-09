from pathlib import Path
from typing import Any, cast

import pandas as pd


def read_transactions_csv(
    file_path: str | Path,
) -> list[dict[str, Any]]:
    """
    Читает транзакции из CSV-файла с разделителем ';'.
    """
    dataframe = pd.read_csv(file_path, sep=";")
    records = dataframe.to_dict(orient="records")

    return cast(list[dict[str, Any]], records)


def read_transactions_excel(
    file_path: str | Path,
) -> list[dict[str, Any]]:
    """
    Читает транзакции из XLSX-файла.
    """
    dataframe = pd.read_excel(file_path)
    records = dataframe.to_dict(orient="records")

    return cast(list[dict[str, Any]], records)
