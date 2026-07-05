import pytest

from my_project.masks import get_mask_card_number, get_mask_account
from my_project.widget import mask_account_card, get_date


# ---------- Фикстуры для исходных данных ----------

@pytest.fixture
def card_number_plain():
    return "7000792289606361"


@pytest.fixture
def card_number_spaced():
    return "7000 7922 8960 6361"


@pytest.fixture
def short_card_number():
    # меньше 10 символов, чтобы проверить "короткий" случай
    return "123456789"


@pytest.fixture
def account_number_long():
    return "73654108430135874305"


@pytest.fixture
def account_number_medium():
    return "1234567890"


@pytest.fixture
def account_number_short():
    return "1234"


@pytest.fixture
def card_raw_line_visa(card_number_plain):
    return f"Visa Platinum {card_number_plain}"


@pytest.fixture
def card_raw_line_master():
    return "MasterCard 1234567812345678"


@pytest.fixture
def account_raw_line(account_number_long):
    return f"Счет {account_number_long}"


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


# ---------- Тесты для masks.py с параметризацией ----------

@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
    ],
)
def test_get_mask_card_number_parametrized(card_number, expected):
    """
    Проверяем маскирование номера карты на разных входных данных:
    - обычная карта,
    - другая карта,
    - карта с пробелами.
    """
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_short_returns_original(short_card_number):
    """
    Проверяем, что при слишком коротком номере карта возвращается без изменений.
    """
    assert get_mask_card_number(short_card_number) == short_card_number


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("1234567890", "**7890"),
    ],
)
def test_get_mask_account_parametrized(account_number, expected):
    """
    Проверяем маскирование номера счета на разных входных данных.
    """
    assert get_mask_account(account_number) == expected


def test_get_mask_account_short_returns_original(account_number_short):
    """
    Проверяем, что при коротком номере счета функция возвращает исходное значение.
    """
    assert get_mask_account(account_number_short) == account_number_short


# ---------- Тесты для widget.py с параметризацией ----------

@pytest.mark.parametrize(
    "raw_data, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
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


def test_mask_account_card_invalid_input_raises_error():
    """
    Проверяем устойчивость к некорректным входным данным:
    строка без пробела должна вызвать ошибку при rsplit.
    """
    with pytest.raises(ValueError):
        mask_account_card("НеверныйВвод")
