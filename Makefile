update:
	@pip install --upgrade pip

install:
	@pip install -r services/web/requirements.txt

install-dev:
	@pip install -r requirements-dev.txt

run:
	@cd services/web/ && gunicorn -w 4 -b 0.0.0.0:5000 main:app

test:
	@python -m pytest

pre-commit:
	@pre-commit install

initial-tag:
	@git tag -a -m "Initial tag." v0.0.1

bump-tag:
	@cz bump --check-consistency --changelog

start-db-containers:
	@sudo docker compose -f services/database/database-compose.yml up --build -d

stop-db-containers:
	@sudo docker compose -f services/database/database-compose.yml down -v

start-vault:
	@sudo docker compose -f services/secrets/vault-compose.yml up --build -d

vault-bash:
	@sudo docker compose exec vault bash

create-db:
	@python services/web/manage.py create_db

seed-db:
	@python services/web/manage.py seed_db

test-local:
	@curl localhost:5000/
	@curl localhost:5000/users

all: update install install-dev pre-commit initial-tag start-db-containers create-db test seed-db run
