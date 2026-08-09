import pytest

from my_project.main import (
    count_operations_by_category,
    filter_operations_by_status,
    filter_rub_operations,
    load_operations,
    main,
    normalize_operation,
    normalize_status,
    parse_sort_direction,
    parse_yes_no,
    search_operations,
    sort_operations_by_date,
)


def test_normalize_json_operation() -> None:
    operation = {
        "id": 1,
        "state": "EXECUTED",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB",
            },
        },
        "description": "Перевод организации",
    }

    result = normalize_operation(operation)

    assert result["amount"] == "31957.58"
    assert result["currency_name"] == "руб."
    assert result["currency_code"] == "RUB"
    assert result["description"] == "Перевод организации"


def test_normalize_csv_operation() -> None:
    operation = {
        "id": 2,
        "state": "EXECUTED",
        "amount": 1000,
        "currency_code": "RUB",
        "currency_name": "Russian Ruble",
        "description": "Оплата",
    }

    result = normalize_operation(operation)

    assert result["id"] == 2
    assert result["state"] == "EXECUTED"
    assert result["amount"] == 1000
    assert result["currency_code"] == "RUB"
    assert result["currency_name"] == "Russian Ruble"
    assert result["description"] == "Оплата"


def test_normalize_operation_preserves_missing_amount() -> None:
    operation = {
        "id": 3,
        "description": "Операция без суммы",
    }

    result = normalize_operation(operation)

    assert result["description"] == "Операция без суммы"
    assert "amount" not in result
    assert "currency_code" not in result


@pytest.mark.parametrize("source", ["1", "2", "3"])
def test_load_operations_from_each_source(source: str) -> None:
    operations = load_operations(source)

    assert operations
    assert all(isinstance(operation, dict) for operation in operations)
    assert all(isinstance(operation.get("description"), str) for operation in operations)


def test_load_operations_rejects_unknown_source() -> None:
    with pytest.raises(ValueError, match="Неизвестный источник"):
        load_operations("4")


def test_filter_operations_by_status_is_case_insensitive() -> None:
    operations = [
        {"state": "EXECUTED", "id": 1},
        {"state": "CANCELED", "id": 2},
        {"state": "EXECUTED", "id": 3},
    ]

    result = filter_operations_by_status(
        operations,
        "executed",
    )

    assert result == [
        {"state": "EXECUTED", "id": 1},
        {"state": "EXECUTED", "id": 3},
    ]


def test_filter_operations_by_status_rejects_invalid_status() -> None:
    operations = [
        {"state": "EXECUTED", "id": 1},
    ]

    with pytest.raises(ValueError, match="недоступен"):
        filter_operations_by_status(operations, "UNKNOWN")


def test_filter_rub_operations() -> None:
    operations = [
        {"currency_code": "RUB", "id": 1},
        {"currency_code": "USD", "id": 2},
        {"currency_code": "RUB", "id": 3},
    ]

    result = filter_rub_operations(operations)

    assert result == [
        {"currency_code": "RUB", "id": 1},
        {"currency_code": "RUB", "id": 3},
    ]


def test_filter_rub_operations_returns_empty_list() -> None:
    operations = [
        {"currency_code": "USD", "id": 1},
        {"currency_code": "EUR", "id": 2},
    ]

    assert filter_rub_operations(operations) == []


def test_sort_operations_by_date_ascending() -> None:
    operations = [
        {"date": "2022-01-01T00:00:00", "id": 2},
        {"date": "2020-01-01T00:00:00", "id": 1},
    ]

    result = sort_operations_by_date(
        operations,
        reverse=False,
    )

    assert [operation["id"] for operation in result] == [1, 2]


def test_sort_operations_by_date_descending() -> None:
    operations = [
        {"date": "2020-01-01T00:00:00", "id": 1},
        {"date": "2022-01-01T00:00:00", "id": 2},
    ]

    result = sort_operations_by_date(
        operations,
        reverse=True,
    )

    assert [operation["id"] for operation in result] == [2, 1]


def test_sort_operations_by_date_ignores_invalid_dates() -> None:
    operations = [
        {"date": "2020-01-01T00:00:00", "id": 1},
        {"date": "", "id": 2},
        {"date": "invalid-date", "id": 3},
        {"date": "2022-01-01T00:00:00", "id": 4},
    ]

    result = sort_operations_by_date(
        operations,
        reverse=False,
    )

    assert [operation["id"] for operation in result] == [1, 4]


def test_normalize_status() -> None:
    assert normalize_status(" executed ") == "EXECUTED"
    assert normalize_status("canceled") == "CANCELED"
    assert normalize_status("pending") == "PENDING"


def test_normalize_status_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="недоступен"):
        normalize_status("UNKNOWN")


@pytest.mark.parametrize(
    "answer",
    ["да", "д", "yes", "y"],
)
def test_parse_yes_no_returns_true(answer: str) -> None:
    assert parse_yes_no(answer) is True


@pytest.mark.parametrize(
    "answer",
    ["нет", "н", "no", "n"],
)
def test_parse_yes_no_returns_false(answer: str) -> None:
    assert parse_yes_no(answer) is False


def test_parse_yes_no_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="Введите"):
        parse_yes_no("maybe")


def test_parse_sort_direction() -> None:
    assert parse_sort_direction("по убыванию") is True
    assert parse_sort_direction("по возрастанию") is False
    assert parse_sort_direction("1") is False
    assert parse_sort_direction("2") is True


def test_parse_sort_direction_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="Введите"):
        parse_sort_direction("3")


def test_search_operations_finds_description() -> None:
    operations = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Оплата услуг"},
    ]

    result = search_operations(
        operations,
        "организации",
    )

    assert result == [
        {"description": "Перевод организации"},
    ]


def test_search_operations_is_case_insensitive() -> None:
    operations = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]

    result = search_operations(
        operations,
        "ПЕРЕВОД",
    )

    assert result == [
        {"description": "Перевод организации"},
    ]


def test_search_operations_supports_regular_expression() -> None:
    operations = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Оплата услуг"},
    ]

    result = search_operations(
        operations,
        "перевод|оплата",
    )

    assert result == [
        {"description": "Перевод организации"},
        {"description": "Оплата услуг"},
    ]


def test_search_operations_returns_all_for_empty_query() -> None:
    operations = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]

    assert search_operations(operations, "") == operations


def test_count_operations_by_category() -> None:
    operations = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
    ]

    result = count_operations_by_category(
        operations,
        [
            "Перевод организации",
            "Открытие вклада",
            "Оплата услуг",
        ],
    )

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Оплата услуг": 0,
    }


def test_count_operations_by_category_ignores_case() -> None:
    operations = [
        {"description": "Перевод организации"},
        {"description": "ПЕРЕВОД ОРГАНИЗАЦИИ"},
        {"description": "Открытие вклада"},
    ]

    result = count_operations_by_category(
        operations,
        ["перевод организации", "Открытие вклада"],
    )

    assert result == {
        "перевод организации": 2,
        "Открытие вклада": 1,
    }


def test_main_success_flow(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    operations = [
        {
            "state": "EXECUTED",
            "date": "2022-01-01T00:00:00",
            "description": "Перевод организации",
            "currency_code": "RUB",
            "currency_name": "руб.",
            "amount": "1000",
            "from": "Visa 1234567890123456",
            "to": "Счет 1234567890",
        },
    ]

    monkeypatch.setattr(
        "my_project.main.load_operations",
        lambda source: operations,
    )

    answers = iter(
        [
            "1",
            "executed",
            "да",
            "по убыванию",
            "да",
            "нет",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers),
    )

    main()

    output = capsys.readouterr().out

    assert "Загружено операций: 1" in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "Перевод организации" in output
    assert "1000 руб." in output


def test_main_invalid_status_and_empty_result(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    operations = [
        {
            "state": "EXECUTED",
            "date": "2022-01-01T00:00:00",
            "description": "Перевод организации",
            "currency_code": "RUB",
            "currency_name": "руб.",
            "amount": "1000",
        },
    ]

    monkeypatch.setattr(
        "my_project.main.load_operations",
        lambda source: operations,
    )

    answers = iter(
        [
            "1",
            "incorrect",
            "EXECUTED",
            "нет",
            "нет",
            "да",
            "оплата",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers),
    )

    main()

    output = capsys.readouterr().out

    assert "недоступен" in output
    assert "Не найдено ни одной транзакции" in output


def test_main_returns_when_loading_fails(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def raise_loading_error(source: str) -> list[dict[str, object]]:
        raise OSError("Ошибка чтения файла")

    monkeypatch.setattr(
        "my_project.main.load_operations",
        raise_loading_error,
    )

    answers = iter(["1"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers),
    )

    main()

    output = capsys.readouterr().out

    assert "Не удалось загрузить операции" in output
