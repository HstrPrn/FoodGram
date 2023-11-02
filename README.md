# Foodgram

Foodgram - удобный вэб сервис, где люди могут делиться своими кулинарными рецептами.
Предусмотрены такие возможности как:
- публикация, редактирование, удаление рецепта
- установка тега
- добавление рецептов в избранное
- возможность скачать список ингредиентов в .csv формате
- подписка на автора рецепта
- регистрация, удаление пользователя
- админка с полным контролем над рецептами и пользователями

# Stack

- [Django 4.2.4](https://docs.djangoproject.com/en/4.2/)
- [DRF 3.14.0](https://www.django-rest-framework.org/community/3.14-announcement/)
- [Djoser 2.2.0](https://djoser.readthedocs.io/en/latest/index.html)
- [PostgreSQL 13](https://www.postgresql.org/files/documentation/pdf/13/postgresql-13-A4.pdf)
- [Nginx 1.19.3](https://nginx.org/en/docs/)
- [Docker 24.0.5](https://docs.docker.com/engine/release-notes/24.0/)

# Локальное развертывание

Клонируйте проект на свой компьютер

    git clone https://github.com/HstrPrn/foodgram-project-react

Запишите переменные окружения в .env. Шаблон для заполнения:

    SECRET_KEY=
    DEBUG=
    ALLOWED_HOSTS=
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    PG_HOST=
    PG_PORT=
    SUPERUSER_USERNAME=
    SUPERUSER_EMAIL=
    SUPERUSER_FIRST_NAME=
    SUPERUSER_LAST_NAME=
    SUPERUSER_PASSWORD=
    CSRF_TRUSTED_ORIGINS=

Запустите docker-compose.yml из корневой директории

    sudo docker compose -f infrs/docker-compose.yml up 

заходите на локальный сервер http://127.0.0.1/

# Примеры работы АПИ
## Создание рецепта

Успешный POST-запрос к эндпоинту api/recipes/

    {
        "ingredients": [
            {
                "id": 0,
                "amount": 0
            }
        ],
        "tags": [
            0
        ],
        "image": "string",
        "name": "string",
        "text": "string",
        "cooking_time": 0
    }

вернет ответ

    {
        "id": 2,
        "tags": [
            {
                "id": 0,
                "name": "string",
                "color": "string",
                "slug": "string"
            }
        ],
        "author": {
            "is_subscribed": bool,
            "username": "string",
            "first_name": "string",
            "last_name": "string",
            "id": 0,
            "email": "string"
        },
        "ingredients": [
            {
                "id": 0,
                "name": "string",
                "measurement_unit": "string",
                "amount": 0
            }
        ],
        "is_favorited": bool,
        "is_in_shopping_cart": bool,
        "name": "string",
        "image": "string",
        "text": "string",
        "cooking_time": 0
    }

## Получение токена авторизации

Успешный POST-запрос к эндпоинту api/auth/token/login/

    {
        "password": "string",
        "email": "string"
    }

вернет ответ

    {
        "auth_token": "string"
    }

## Подписки, подписаться

Успешный пустой POST-запрос к эндпоинту api/users/2/subscribe/ вернет ответ

    {
        "recipes": [],
        "recipes_count": 0,
        "is_subscribed": bool,
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "id": 0,
        "email": "string"
    }

### Документация

Подробную документацию можно найти, запустив проект с параметром перейдя по адресу http://127.0.0.1/api/docs/

# Авторы

[Иван Ефремов](https://github.com/HstrPrn)
