.PHONY:install-pre-commit
install-pre-commit:
	pre-commit uninstall; pre-commit install 

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY:packages
packages:
	pip install -r requirements.txt

.PHONY:migrate
migrate:
	python manage.py migrate

.PHONY:migrations
migrations:
	python manage.py makemigrations

.PHONY:runserver
runserver:
	python manage.py runserver

.PHONY:superuser
superuser:
	python manage.py createsuperuser

.PHONY:setup
setup: install migrations migrate install-pre-commit ;

.PHONY:coverage-test
coverage-test:
	python manage.py test

.PHONY:coverage-report
coverage-report:
	coverage report

.PHONY:coverage-html
coverage:
	coverage html

.PHONY:run-coverage
run-coverage: coverage-test coverage-report coverage-html ;