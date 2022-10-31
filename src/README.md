# Код Flask-приложения

## Локальный запуск
Предварительно необходимо создать файл `core/.env` со следующими параметрами:

- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- PG_HOST - хост Postgres
- PG_PORT - порт Postgres
- PG_DB_NAME - название бд Postgres
- PG_USER - имя пользователя Postgres
- PG_PASSWORD - пароль Postgres

Для запуска api необходимо выполнить команду
```python src/app.py```
