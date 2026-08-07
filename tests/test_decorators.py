# my-project/tests/test_decorators.py

import pytest

from my_project.decorators import log


def test_log_success_console(capsys):
    @log()
    def add(x, y):
        return x + y

    result = add(1, 2)

    # проверяем результат функции
    assert result == 3

    # перехватываем вывод в консоль
    captured = capsys.readouterr()
    # ожидаемый формат: "<имя функции> ok"
    assert captured.out.strip() == "add ok"
    assert captured.err == ""


def test_log_error_console(capsys):
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    # ожидаемый формат: "divide error: ZeroDivisionError. Inputs: (1, 0), {}"
    out = captured.out.strip()
    assert out.startswith("divide error: ZeroDivisionError. Inputs: (1, 0), {}")
    assert captured.err == ""

    def test_log_success_file(tmp_path):
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def add(x, y):
            return x + y

        result = add(1, 2)
        assert result == 3

        # читаем файл и проверяем содержимое
        content = log_file.read_text(encoding="utf-8").strip()
        assert content == "add ok"

    def test_log_error_file(tmp_path):
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def divide(x, y):
            return x / y

        with pytest.raises(ZeroDivisionError):
            divide(1, 0)

        content = log_file.read_text(encoding="utf-8").strip()
        # формат: "divide error: ZeroDivisionError. Inputs: (1, 0), {}"
        assert content.startswith("divide error: ZeroDivisionError. Inputs: (1, 0), {}")
