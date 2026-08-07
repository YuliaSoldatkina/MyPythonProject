# tests/test_masks.py

import pytest

from my_project.masks import get_mask_account, get_mask_card_number

# ---------- Фикстуры для масок ----------


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


# ---------- Тесты для get_mask_card_number ----------


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
    Проверяем, что при слишком коротком
    номере карта возвращается без изменений.
    """
    assert get_mask_card_number(short_card_number) == short_card_number


# ---------- Тесты для get_mask_account ----------


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
    Проверяем, что при коротком номере счета
    функция возвращает исходное значение.
    """
    assert get_mask_account(account_number_short) == account_number_short
