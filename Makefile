prepare_environment:
	cp -r env.example .env
	pip install -r admin_panel/requirements.txt

run_postgres:
	docker compose up -d postgres pgadmin

run_environment: run_postgres

drop_db:
	docker stop postgres_container && docker rm --force postgres_container
	docker volume rm admin_panel_postgres

run_project:
	python3 admin_panel/manage.py migrate
	python3 admin_panel/manage.py runserver

create_django_superuser:
	python admin_panel/manage.py createsuperuser