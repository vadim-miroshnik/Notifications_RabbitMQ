prepare_environment:
	cp -r env.example .env
	pip install -r admin_panel/requirements.txt

run_postgres:
	docker compose up -d postgres pgadmin

run_mongodb:
	docker-compose -f docker-compose_mongodb.yml up -d

run_environment: run_postgres run_mongodb

drop_db:
	docker stop postgres_container && docker rm --force postgres_container
	docker volume rm admin_panel_postgres

run_project:
	python3 admin_panel/manage.py migrate
	python3 admin_panel/manage.py runserver

create_django_superuser:
	python admin_panel/manage.py createsuperuser

initialize_mongo:
	backoff/mongo/wait_for_up.sh
	docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
	docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
	docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
	docker exec -it mongors1n1 bash -c 'echo "use movies" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"movies\")" | mongosh'

run_rabbit:
	docker compose up -d rabbitmq
