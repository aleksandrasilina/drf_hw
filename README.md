Платформа для онлайн-обучения

Для запуска проекта необходимо:
1. создать файл .env со своими данными по образцу .env.sample
2. запустить redis-серевер
3. запустить celery worker для запуска отложенных задач командой:
celery -A config worker -l INFO -P eventlet
4. запустить celery beat для запуска периодических задач командой:
celery -A config beat -l info -S django


Наполнение базы данных lms (уроки, курсы):
python manage.py loaddata lms.json 

Наполнение базы данных users (пользователи, платежи):
python manage.py loaddata users.json

Создание групп:
python manage.py loaddata groups.json 


Запуск проекта в Docker контейнере:
docker compose up -d --build