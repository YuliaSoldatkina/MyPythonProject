# MyPythonProject

Проект содержит функции для маскирования номеров карт и счетов, форматирования дат, а также обработки операций.

## Структура проекта

- `src/my_project/masks.py` — функции маскирования номера карты и счёта.
- `src/my_project/widget.py` — функции форматирования данных карты/счёта и даты.
- `src/my_project/processing.py` — функции фильтрации операций по статусу и сортировки по дате.
- `tests/` — тесты для модулей проекта.

## Тестирование

В проекте используются тесты на основе библиотеки `pytest`.

Тесты разделены по модулям:
- `tests/test_masks.py` — тесты для `src/my_project/masks.py`
- `tests/test_widget.py` — тесты для `src/my_project/widget.py`
- `tests/test_processing.py` — тесты для `src/my_project/processing.py`

Запуск всех тестов:

```bash
python -m pytest
```

Проверка покрытия кода:

```bash
python -m pytest --cov=src/my_project
```