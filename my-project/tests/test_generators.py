import pytest
from my_project.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)


@pytest.fixture
def transactions_sample():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2019-04-05T23:20:05.206878",
            "operationAmount": {
                "amount": "10.00",
                "currency": {"name": "RUB", "code": "RUB"},
            },
            "description": "Перевод с карты на карту",
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "date": "2019-04-06T23:20:05.206878",
            "operationAmount": {
                "amount": "1.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
        },
    ]


# ---------- filter_by_currency ----------

def test_filter_by_currency_iterator(transactions_sample):
    usd_transactions = filter_by_currency(transactions_sample, "USD")

    first = next(usd_transactions)
    second = next(usd_transactions)

    assert first["id"] == 939719570
    assert second["id"] == 142264268


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [939719570, 142264268, 4]),
        ("RUB", [3]),
        ("EUR", []),
    ],
)
def test_filter_by_currency_parametrized(transactions_sample, currency, expected_ids):
    result = list(filter_by_currency(transactions_sample, currency))
    ids = [tx["id"] for tx in result]
    assert ids == expected_ids


def test_filter_by_currency_empty_list():
    assert list(filter_by_currency([], "USD")) == []


# ---------- transaction_descriptions ----------

def test_transaction_descriptions_sequence(transactions_sample):
    descriptions = transaction_descriptions(transactions_sample)

    result = [next(descriptions) for _ in range(4)]
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


def test_transaction_descriptions_empty():
    assert list(transaction_descriptions([])) == []


def test_transaction_descriptions_missing_key():
    transactions = [{"id": 1}, {"description": "Есть описание"}]
    result = list(transaction_descriptions(transactions))
    assert result == ["", "Есть описание"]


# ---------- card_number_generator ----------

def test_card_number_generator_small_range():
    gen = card_number_generator(1, 5)
    assert list(gen) == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


def test_card_number_generator_bounds():
    gen = card_number_generator(0, 2)
    assert list(gen) == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
    ]


def test_card_number_generator_last_number():
    gen = card_number_generator(9_999_999_999_999_999, 9_999_999_999_999_999)
    assert list(gen) == ["9999 9999 9999 9999"]
