# tests/test_processing.py

import pytest

from my_project.processing import filter_by_state, sort_by_date

# ---------- Фикстура со списком операций ----------


@pytest.fixture
def operations_sample():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-11T02:26:18.671407",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2023-01-01T00:00:00",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-03-10T10:00:00",
        },
        {
            "id": 4,
            "state": "PENDING",
            "date": "2024-03-09T12:00:00",
        },
    ]


# ---------- Тесты filter_by_state с параметризацией ----------


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(operations_sample, state, expected_ids):
    """
    Проверяем фильтрацию по статусу state, включая случай,
    когда операций с таким статусом нет.
    """
    result = filter_by_state(operations_sample, state)
    result_ids = [op["id"] for op in result]
    assert result_ids == expected_ids


# ---------- Тесты sort_by_date ----------


def test_sort_by_date_descending(operations_sample):
    """
    Проверяем сортировку по дате в порядке убывания (reverse=True по умолчанию).
    Самая новая дата должна быть первой.
    """
    result = sort_by_date(operations_sample)  # reverse=True
    result_ids = [op["id"] for op in result]
    # ожидаем порядок: 1 (11 марта), 3 (10 марта), 4 (9 марта), 2 (1 янв 2023)
    assert result_ids == [1, 3, 4, 2]


def test_sort_by_date_ascending(operations_sample):
    """
    Проверяем сортировку по дате в порядке возрастания.
    """
    result = sort_by_date(operations_sample, reverse=False)
    result_ids = [op["id"] for op in result]
    assert result_ids == [2, 4, 3, 1]


def test_sort_by_date_same_dates():
    """
    Проверяем корректность сортировки при одинаковых датах:
    порядок среди одинаковых дат должен быть стабильным.
    """
    operations = [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-10T10:00:00"},
    ]
    result = sort_by_date(operations)  # убывание
    result_ids = [op["id"] for op in result]
    assert result_ids == [1, 2, 3]


def test_sort_by_date_invalid_format_raises_error():
    """
    Проверяем работу функции с некорректным форматом даты:
    datetime.fromisoformat должен вызвать ValueError.
    """
    operations = [
        {"id": 1, "state": "EXECUTED", "date": "11.03.2024"},
    ]
    with pytest.raises(ValueError):
        sort_by_date(operations)
