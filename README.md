# 📰📺 медиа-сервис новостной в Telegram | NewsBot | Python, Django, PostgresSQL, DRF, Docker, Nginx, Aiogram, Redis


## Суть приложения

Каждый пользователь может иметь статус обычного пользователя или администратора.
Администратор имеет доступ к админ-панели, в то время как пользователь - нет.
Реализация этой задачи может быть различной.
Каждый пользователь может создавать публикации.
Все пользователи могут просматривать список всех публикаций.
Пользователи могут удалять и изменять свои собственные новости, а администратор может управлять любыми новостями.
Необходимо также добавить механизм для лайков и комментариев к новостям.
Лайк и комментарий может оставлять любой пользователь.
Автор может удалять комментарии к своим новостям, а администратор может удалять любые комментарии.
При запросе списка публикаций или одной конкретной новости должно отображаться количество лайков и комментариев.


# Локальный Swagger
```http request
GET api/schema/swagger-ui/
```

## Как запустить
* склонируйте репозиторий ``` git clone https://github.com/Pavel2232/NewsBot  ```
* создайте виртуальное окружение проекта ```poetry shell ```
* установите зависимости проекта ```poetry install ```
* заполните .env по аналогии с [.env.example](.env.example)
* выполните ```python manage.py makemigrations```
* выполните ```python manage.py migrate```
* по желанию можете загрузить тестовые данные ```python manage.py loaddata db.json```
* выполните ```python manage.py runserver```

## Как запустить через Docker
* склонируйте репозиторий ``` git clone https://github.com/Pavel2232/NewsBot  ```
* заполните .env по аналогии с [.env.example](.env.example)
* выполните ```docker compose up -d ```
* сервер будет доступен по адресу ```http://localhost/```

