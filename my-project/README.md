# MyPythonProject

Проект для обработки финансовых транзакций.

## Возможности

- Загрузка транзакций из JSON-файлов (`utils.load_transactions`)
- Конвертация транзакций из USD/EUR в рубли через внешний API (`external_api.convert_transaction_to_rub`)

## Установка

```bash
poetry install
```

## Использование

```bash
poetry run pytest
```

## Переменные окружения

Создайте файл `.env` в корне проекта:

```ini
EXCHANGE_RATE_API_KEY=ваш_api_key
```

## Тесты

```bash
poetry run pytest
```