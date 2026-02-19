# API для Yatube

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Django](https://img.shields.io/badge/Django-3.2-green)
![DRF](https://img.shields.io/badge/DRF-3.12-red)
![JWT](https://img.shields.io/badge/JWT-auth-orange)

## Описание

API для социальной сети Yatube. Проект реализован в рамках учебного курса Яндекс.Практикума.

### Возможности
- JWT-аутентификация
- Публикация постов с изображениями
- Комментирование постов
- Создание и просмотр сообществ
- Подписка на авторов
- Пагинация с параметрами limit/offset
- Поиск по подпискам

## Технологии

- Python 3.9
- Django 3.2
- Django REST Framework 3.12
- Simple JWT
- SQLite3
- Pytest

## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/GermanSkvortsov/api-final-yatube.git
cd api-final-yatube
```

### 2. Создать и активировать виртуальное окружение

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Выполнить миграции
```bash
cd yatube_api
python manage.py migrate
```

### 5. Запустить сервер
```bash
python manage.py runserver
```

### 6. Открыть документацию
После запуска документация доступна по адресу:
http://127.0.0.1:8000/redoc/

## Примеры запросов

### Получение JWT-токена
```bash
POST /api/v1/jwt/create/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Ответ:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```


### Создание поста
```bash
POST /api/v1/posts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "text": "Мой первый пост!",
    "group": 1
}
```

**Ответ:**
```json
{
    "id": 1,
    "author": "your_username",
    "text": "Мой первый пост!",
    "pub_date": "2024-01-01T12:00:00Z",
    "image": null,
    "group": 1
}
```

### Получение списка постов с пагинацией
```bash
GET /api/v1/posts/?limit=2&offset=0
```

**Ответ:**
```json
{
    "count": 15,
    "next": "http://127.0.0.1:8000/api/v1/posts/?limit=2&offset=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "user1",
            "text": "Первый пост",
            "pub_date": "2024-01-01T12:00:00Z",
            "image": null,
            "group": 1
        },
        {
            "id": 2,
            "author": "user2",
            "text": "Второй пост",
            "pub_date": "2024-01-02T12:00:00Z",
            "image": null,
            "group": 1
        }
    ]
}
```

### Добавление комментария
```bash
POST /api/v1/posts/1/comments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "text": "Отличный пост!"
}
```

**Ответ:**
```json
{
    "id": 1,
    "author": "your_username",
    "post": 1,
    "text": "Отличный пост!",
    "created": "2024-01-01T12:05:00Z"
}
```

### Получение подписок с поиском
```bash
GET /api/v1/follow/?search=username
Authorization: Bearer <access_token>
```

### Подписка на пользователя
```bash
POST /api/v1/follow/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "following": "username"
}
```

## Запуск тестов

В проекте есть готовые тесты в папке `tests/`. Для их запуска выполните:

```bash
pytest
```
Также можно импортировать коллекцию запросов из папки `postman_collection/` в Postman для ручного тестирования.

## Структура проекта

```
api-final-yatube/
├── api/                    # приложение API
│   ├── permissions.py      # кастомные права доступа
│   ├── serializers.py      # сериализаторы
│   ├── urls.py             # маршруты API
│   └── views.py            # вьюсеты
├── posts/                  # приложение с моделями
│   ├── models.py           # модели Post, Comment, Group, Follow
│   └── migrations/         # миграции БД
├── tests/                  # автоматические тесты
├── postman_collection/     # коллекция для Postman
├── yatube_api/             # настройки проекта
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt
```

## Права доступа

- Анонимные пользователи — только чтение (GET) для постов, комментариев и групп
- Авторизованные пользователи — могут создавать посты и комментарии
- Авторы — могут изменять и удалять свои посты и комментарии
- Подписки (/follow/) — только для авторизованных пользователей

## Автор

[Герман Скворцов]  
GitHub: [@GermanSkvortsov](https://github.com/GermanSkvortsov)

## Лицензия

Проект выполнен в учебных целях в рамках курса Яндекс.Практикума.
