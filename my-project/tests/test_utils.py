import json
import tempfile
from pathlib import Path
from my_project.utils import load_transactions


def test_load_transactions_valid():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([{"id": 1, "amount": "100"}], f)
        temp_path = f.name

    result = load_transactions(temp_path)
    assert result == [{"id": 1, "amount": "100"}]


def test_load_transactions_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("")
        temp_path = f.name

    result = load_transactions(temp_path)
    assert result == []


def test_load_transactions_not_list():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"id": 1}, f)
        temp_path = f.name

    result = load_transactions(temp_path)
    assert result == []


def test_load_transactions_file_not_found():
    result = load_transactions("nonexistent_file.json")
    assert result == []
