# MyPythonProject

Небольшой учебный проект для работы со списком операций и практики использования Git и GitHub.

## Цель проекта

Проект показывает, как:
- отфильтровать список операций по статусу (`state`);
- отсортировать операции по дате (`date`).

Все функции находятся в модуле `processing` в директории `src`.

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/YuliaSoldatkina/MyPythonProject.git
   ```

2. Перейдите в папку проекта:
   ```bash
   cd MyPythonProject
   ```

3. При необходимости создайте и активируйте виртуальное окружение.

## Использование функций

### filter_by_state

Функция `filter_by_state` принимает список словарей и возвращает только те элементы, у которых ключ `state` имеет нужное значение.  
По умолчанию используется статус `'EXECUTED'`.

Пример использования:

```python
from processing import filter_by_state

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
]

executed_operations = filter_by_state(operations)
canceled_operations = filter_by_state(operations, state="CANCELED")
```

### sort_by_date

Функция `sort_by_date` принимает список словарей и возвращает новый список, отсортированный по ключу `date`.  
По умолчанию сортировка идёт по убыванию — сначала самые поздние даты.

Пример использования:

```python
from processing import sort_by_date

operations = [
    {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
    },
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
    },
    {
        "id": 615064591,
        "state": "CANCELED",
        "date": "2018-10-14T08:21:33.419441",
    },
]

sorted_desc = sort_by_date(operations)               # по убыванию (по умолчанию)
sorted_asc = sort_by_date(operations, reverse=False)  # по возрастанию
```

## Примеры результата

Пример входных данных:

```python
operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
]
```

Результат `filter_by_state(operations)`:

```text
{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
```

Результат `filter_by_state(operations, state="CANCELED")`:

```text
{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
{'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
```

Результат `sort_by_date(operations)` (по убыванию):

```text
{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
{'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
```

## Автор

Yulia Soldatkina