# Makefile for latin-macronizer

requirements.txt: pyproject.toml
	pip-compile -o requirements.txt pyproject.toml

requirements-dev.txt: pyproject.toml
	pip-compile -o requirements-dev.txt pyproject.toml --extra development

.PHONY: upgrade-requirements
upgrade-requirements:
	pip-compile --upgrade -o requirements.txt pyproject.toml
	pip-compile --upgrade -o requirements-dev.txt pyproject.toml --extra development

.PHONY: docker
docker: requirements.txt
	docker build -t latin-macronizer .

.PHONY: run-dev
run-dev:
	gunicorn --reload macronizer.wsgi:app
