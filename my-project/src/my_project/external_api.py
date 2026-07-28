import os
from typing import Dict, Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(currency: str) -> float:
    """
    Получает текущий курс валюты к RUB через API.
    Возвращает курс (сколько RUB за 1 unit валюты).
    """
    headers = {
        "apikey": API_KEY,
    }
    params = {
        "base": currency,
        "symbols": "RUB",
    }
    response = requests.get(
        BASE_URL, headers=headers, params=params, timeout=10
    )
    response.raise_for_status()
    data = response.json()
    return float(data["rates"]["RUB"])


def convert_transaction_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях (float).

    Если валюта RUB — просто возвращает amount.
    Если USD или EUR — конвертирует через API.
    """
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    if currency in ("USD", "EUR"):
        rate = get_exchange_rate(currency)
        return amount * rate

    # Если валюта другая, просто возвращаем amount как есть
    return amount
