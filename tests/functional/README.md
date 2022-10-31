# Код функциональных тестов

## Локальный запуск
Предварительно необходимо создать файл `tests/functional/.env` со следующими параметрами:

- FLASK_URL - адрес сервиса авторизации
- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- PG_HOST - хост Postgres
- PG_PORT - порт Postgres
- PG_DB_NAME - название бд Postgres
- PG_USER - имя пользователя Postgres
- PG_PASSWORD - пароль Postgres

Для запуска тестов необходимо выполнить команду
```pytest ./tests/functional/src```


## Запуск в Docker
Предварительно необходимо создать файл `tests/functional/docker.env` со следующими параметрами:

- FLASK_URL - адрес сервиса авторизации
- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- PG_HOST - хост Postgres
- PG_PORT - порт Postgres
- PG_DB_NAME - название бд Postgres
- PG_USER - имя пользователя Postgres
- PG_PASSWORD - пароль Postgres

Для запуска api необходимо выполнить команду
```docker compose up --build```