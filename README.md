# Проектная работа 10 спринта

Запуск админки:

    make prepare_environment
    make run_postgres
    python admin_panel/manage.py migrate
    python admin_panel/manage.py collectstatic
    make run_project

Запуск сервиса нотификации:

    make run_mongodb
    make initialize_mongo
    ...

Запуска сендера писем:
    
    ...


Проектные работы в этом модуле в команде. Задания на спринт вы найдёте внутри тем.
