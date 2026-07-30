"""Утилиты для обработки транзакций."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def load_transactions(filepath: str) -> List[Dict[str, Any]]:
    """
    Загружает список финансовых транзакций из JSON-файла.

    Если файл не найден, пустой, или в нём не список,
    возвращает пустой список.
    """
    logger.info("Загрузка транзакций из %s", filepath)
    path = Path(filepath)

    if not path.exists():
        logger.warning("Файл не найден: %s", filepath)
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error("Ошибка при чтении файла: %s", e)
        return []

    if not isinstance(data, list):
        logger.warning("Файл содержит не список")
        return []

    logger.info("Загружено %d транзакций", len(data))
    return data
