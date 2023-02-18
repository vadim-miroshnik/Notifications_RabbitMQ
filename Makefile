prepare_environment:
	cp -r env.example .env
	pip install -r admin_panel/requirements.txt
	pip install -r notification_api/requirements.txt

run_postgres:
	docker compose \
		-f docker-compose_network.yml \
		-f docker-compose.yml \
		-f docker-compose.override.yml \
		up -d postgres pgadmin

run_mongodb:
	docker compose \
		-f docker-compose_network.yml \
		-f docker-compose_mongodb.yml \
		-f docker-compose_mongodb.override.yml \
		up -d

drop_db:
	docker stop postgres_container && docker rm --force postgres_container
	docker volume rm admin_panel_postgres

run_project:
	python3 admin_panel/manage.py migrate
	python3 admin_panel/manage.py makemessages -l en -l ru
	python3 admin_panel/manage.py compilemessages -l en -l ru
	python3 admin_panel/manage.py runserver

run_admin_panel:
	docker compose \
		-f docker-compose_network.yml \
 		-f docker-compose.yml \
		-f docker-compose.override.yml \
 		up --build admin

run_notification_container:
	docker compose \
		-f docker-compose_network.yml \
 		-f docker-compose.yml \
		-f docker-compose.override.yml \
 		up --build notification

run_worker:
	docker compose \
		-f docker-compose_network.yml \
 		-f docker-compose.yml \
		-f docker-compose.override.yml \
 		up --build worker

run_scheduler:
	docker compose \
		-f docker-compose_network.yml \
 		-f docker-compose.yml \
		-f docker-compose.override.yml \
 		up --build scheduler


create_django_superuser:
	python3 admin_panel/manage.py createsuperuser

initialize_mongo: run_mongodb
	backoff/mongo/wait_for_up.sh
	docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
	docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
	docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
	docker exec -it mongors1n1 bash -c 'echo "use movies" | mongosh'
	backoff/mongo/wait_for_up_step2.sh
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"movies\")" | mongosh'

run_rabbit:
	docker compose \
		-f docker-compose_network.yml \
		-f docker-compose.yml \
		 up -d rabbitmq

run_environment: run_postgres run_mongodb run_rabbit

down:
	docker compose \
		-f docker-compose_network.yml \
		-f docker-compose.yml \
		-f docker-compose.override.yml \
		-f docker-compose_mongodb.yml \
		-f docker-compose_mongodb.override.yml \
		down --remove-orphans

run_prod:
	docker compose \
		-f docker-compose_network.yml \
		-f docker-compose.yml \
		-f docker-compose_mongodb.yml \
		up -d
