# Aleksey Khadkov
## Homework 23.2

## Для подключения данных создать файл `.env`, добавить в него :

- DB_HOST=localhost  # или 127.0.0.1:8000 / хост бд
- DB_USER=postgres  # пользователь бд
- DB_PASSWORD=12345  # пароль пользователя от бд
- DB_NAME='distribution'  # название бд
- DB_ENGINE='django.db.backends.postgresql_psycopg2'  # подключение бд
- EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
- EMAIL_HOST='smtp.yandex.ru'  # для яндекс почты
- EMAIL_PORT=465  # для яндекс почты
- EMAIL_HOST_USER='your_email@yandex.ru'
- EMAIL_HOST_PASSWORD='your_yandex_smtp_password'

## В файле `users/management/commands/csu.py` команда для создания суперпользователя с паролем 12345 . запустить команду `python manage.py csu`

## Загрузить тестовые статьи из блога `python manage.py loaddata blog_data.json`.

## Загрузить тестовые продукты из каталога `python manage.py loaddata catalog_dеata.json`.

## Зайдя суперпользователем во вкладке `Users` есть кнопка для создания модератора

## В приложении `main` файл `services` 
