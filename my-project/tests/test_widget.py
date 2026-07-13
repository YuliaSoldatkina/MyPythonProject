# tests/test_widget.py

import pytest
from my_project.widget import mask_account_card, get_date


# ---------- Фикстуры для widget ----------

@pytest.fixture
def card_raw_line_visa():
    return "Visa Platinum 7000792289606361"


@pytest.fixture
def card_raw_line_master():
    return "MasterCard 1234567812345678"


@pytest.fixture
def account_raw_line():
    return "Счет 73654108430135874305"


@pytest.fixture
def valid_iso_date():
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def another_iso_date():
    return "2023-01-01T00:00:00"


@pytest.fixture
def invalid_date_string():
    # не ISO-формат, должен вызвать ValueError
    return "11.03.2024"


# ---------- Тесты для mask_account_card ----------

@pytest.mark.parametrize(
    "raw_data, expected",
    [
        ("Visa Platinum 7000792289606361",
         "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 1234567812345678",
         "MasterCard 1234 56** **** 5678"),
    ],
)
def test_mask_account_card_for_cards(raw_data, expected):
    """
    Проверяем, что для строк с данными карты функция применяет маску карты.
    """
    assert mask_account_card(raw_data) == expected


def test_mask_account_card_for_account(account_raw_line):
    """
    Проверяем, что для строки, начинающейся с 'Счет',
    функция применяет маску счета.
    """
    assert mask_account_card(account_raw_line) == "Счет **4305"


def test_mask_account_card_invalid_input_raises_error():
    """
    Проверяем устойчивость к некорректным входным данным:
    строка без пробела должна вызвать ошибку при rsplit.
    """
    with pytest.raises(ValueError):
        mask_account_card("НеверныйВвод")


# ---------- Тесты для get_date ----------

def test_get_date_valid_formats(valid_iso_date, another_iso_date):
    """
    Проверяем преобразование корректных ISO-дат в формат 'дд.мм.гггг'.
    """
    assert get_date(valid_iso_date) == "11.03.2024"
    assert get_date(another_iso_date) == "01.01.2023"


def test_get_date_invalid_format_raises_error(invalid_date_string):
    """
    Проверяем, что при некорректном формате даты генерируется ValueError.
    """
    with pytest.raises(ValueError):
        get_date(invalid_date_string)
