from my_project.processing import (
    process_bank_operations,
    process_bank_search,
)

OPERATIONS = [
    {"description": "Перевод с карты на карту"},
    {"description": "Оплата телефона"},
    {"description": "перевод организации"},
    {"description": "Открытие вклада"},
    {"description": None},
]


def test_process_bank_search_is_case_insensitive() -> None:
    result = process_bank_search(OPERATIONS, "ПЕРЕВОД")

    assert result == [
        {"description": "Перевод с карты на карту"},
        {"description": "перевод организации"},
    ]


def test_process_bank_search_supports_regular_expression() -> None:
    result = process_bank_search(OPERATIONS, r"карты|телефона")

    assert result == [
        {"description": "Перевод с карты на карту"},
        {"description": "Оплата телефона"},
    ]


def test_process_bank_search_returns_empty_list_when_nothing_found() -> None:
    assert process_bank_search(OPERATIONS, "кредит") == []


def test_process_bank_operations_counts_categories() -> None:
    result = process_bank_operations(
        OPERATIONS,
        ["Перевод с карты на карту", "Оплата телефона", "Снятие наличных"],
    )

    assert result == {
        "Перевод с карты на карту": 1,
        "Оплата телефона": 1,
        "Снятие наличных": 0,
    }


def test_process_bank_operations_is_case_insensitive() -> None:
    result = process_bank_operations(
        OPERATIONS,
        ["ПЕРЕВОД ОРГАНИЗАЦИИ"],
    )

    assert result == {
        "ПЕРЕВОД ОРГАНИЗАЦИИ": 1,
    }
