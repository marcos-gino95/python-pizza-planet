VENV_NAME= .venv

create-venv:
	python3 -m venv $(VENV_NAME)
	chmod +x $(VENV_NAME)/bin/activate
	. $(VENV_NAME)/bin/activate

create-venv-windows:
	python3 -m venv $(VENV_NAME)
	cd $(VENV_NAME)/Scripts/
	activate

activate-venv:
	 . $(VENV_NAME)/bin/activate && \
    echo "Virtual environment activated: $(VENV_NAME)"

install-dependencies:
	pip install -r requirements.txt

format:
	black app/*
	isort  app/*
	flake8  app/*

test:
	pytest --cov --cov-fail-under=80

init-db:
	python3 manage.py db init
	python3 manage.py db migrate
	python3 manage.py db upgrade

delete-db:
	rm -rf migrations
	rm pizza.sqlite

start-app:
	python3 manage.py run