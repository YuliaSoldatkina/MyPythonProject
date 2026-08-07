from unittest.mock import MagicMock, patch

import pytest

from my_project.external_api import convert_transaction_to_rub


@patch("my_project.external_api.requests.get")
def test_convert_transaction_to_rub(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "rates": {"RUB": 78.448937},
    }
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD", "name": "USD"},
        },
    }

    result = convert_transaction_to_rub(transaction)

    assert result == pytest.approx(7844.8937)
    mock_get.assert_called_once()
