import json
from pathlib import Path
from typing import List, Dict, Any


def load_transactions(filepath: str) -> List[Dict[str, Any]]:
    """
    Загружает список финансовых транзакций из JSON-файла.

    Если файл не найден, пустой, или в нём не список,
    возвращает пустой список.
    """
    path = Path(filepath)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return data
