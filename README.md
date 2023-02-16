# Проектная работа 10 спринта

https://github.com/dimkaddi/notifications_sprint_1

Запуск окружения (Postgres, MongoDB, RabbitMQ):

    make run_environment
Запуск БД Postgres:

    make run_postgres
Удаление базы данных:

    make drop_db
Создание суперпользователя Django:

    make create_django_superuser
## Панель администратора

Через панель администратора осуществляется ввод пользователей, групп рассылки и шаблонов для генерации содержимого сообщений

Запуск проекта панели администратора с миграцией и локализацией:

    make run_project
Запуск проекта в контейнере: 
    
    make run_admin_panel
## Сервис нотификации

Сервис нотификации формирует объект для групповой и персонализирпованной рассылки. Объект включает в себя:
- идентификатор рассылки
- тип транспорта (email, websocket и т.д.)
- шаблон для генерации контента
- приоритет
- тема сообщения
- список получателей (имя, адрес, данные для наполнения, короткая ссылка для обратной связи)

Объект передается в очередь сообщений.

Запуск MongoDB:

    make run_mongodb
Инициализация кластера MongoDB:

    make run_initialize_mongo
Запуск сервера очередей RabbitMQ:

    make run_rabbit
Запуск сервиса уведомлений:

    make run_notification_container

Доступ к openapi сервиса notifications: http://127.0.0.1/api/openapi
Доступ к очереди: http://127.0.0.1:15672/

Для запуска сервиса в проде (отключить проброс портов сервиса и запустить nginx):

    make run_prod
## Компонент формирования и пересылки уведомлений
Компонент читает очередь сообщений, на основе шаблона и данных для контента формирует текст, который передается на отсылку соответствующим транспортом.
Запуск сендера:

    make run_worker

Остановка всех контейнеров:

    make down

## Компонент планировщика
Формирует задачу на email-рассылку для пользователей, входящих в группу common с темплейтом "RegularNotify" каждую пятницу в 17:00

Запуск:

    make run_scheduler

Остановка всех контейнеров:

    make down