# Код Flask-приложения

## Локальный запуск
Предварительно необходимо создать файл `src/core/.env` со следующими параметрами:

- SERVICE_HOST - хост сервиса авторизации
- SERVICE_PORT - порт сервиса авторизации
- DEBUG - флаг запуска сервиса авторизации в debug режиме
- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- PG_HOST - хост Postgres
- PG_PORT - порт Postgres
- PG_DB_NAME - название бд Postgres
- PG_USER - имя пользователя Postgres
- PG_PASSWORD - пароль Postgres

Для запуска api необходимо выполнить команду
```python src/app.py```


## Запуск в Docker
Предварительно необходимо создать файл `src/core/docker.env` со следующими параметрами:

- SERVICE_HOST - хост сервиса авторизации
- SERVICE_PORT - порт сервиса авторизации
- DEBUG - флаг запуска сервиса авторизации в debug режиме
- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- PG_HOST - хост Postgres
- PG_PORT - порт Postgres
- PG_DB_NAME - название бд Postgres
- PG_USER - имя пользователя Postgres
- PG_PASSWORD - пароль Postgres

Для запуска api необходимо выполнить команду
```docker compose up --build```

## Применение миграций
Перед запуском приложения необходимо применить миграции БД
 из каталога с файлом app.py:
 
`  flask db upgrade`

## Создание суперпользователя
Для создания суперпользователя необходимо выполнить команду:
```
cd src
flask create-user login_example password_example example@email.ru
```