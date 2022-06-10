update:
	@pip install --upgrade pip

install:
	@pip install -r requirements.txt

install-dev: requirements-dev.txt
	@pip install -r requirements-dev.txt

run:
	@python main.py

test:
	@python -m pytest

build:
	@docker build -t ${imagename}:latest .

run-docker:
	@sudo docker run --env FLASK_ENV=development -p 5000:5000 ${imagename}:latest

pre-commit:
	@pre-commit install

initial-tag:
	@git tag -a -m "Initial tag." v0.0.1

bump-tag:
	@cz bump
	@cz changelog

all: update install install-dev pre-commit tag test run
