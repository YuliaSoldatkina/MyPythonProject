## Модуль generators

Модуль `src/my_project/generators.py` содержит генераторы для обработки данных.

### filter_by_currency

Генератор, который выдаёт транзакции с указанной валютой:

```python
from my_project.generators import filter_by_currency

transactions = [
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
]

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))
```

### transaction_descriptions

Генератор, который возвращает описания операций по очереди:

```python
from my_project.generators import transaction_descriptions

transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод с карты на карту"},
    {"description": "Перевод организации"},
]

descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
```

### card_number_generator

Генератор номеров карт:

```python
from my_project.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
```
