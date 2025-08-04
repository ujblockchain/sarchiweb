.PHONY:install
install:
	poetry install


.PHONY:install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install 


.PHONY: lint
lint:
	poetry run pre-commit run --all-files


.PHONY:migrate
migrate:
	poetry run python -m core.manage migrate


.PHONY:migrations
migrations:
	poetry run python -m core.manage makemigrations


.PHONY:collectstatic
collectstatic:
	poetry run python -m core.manage collectstatic


.PHONY:runserver
runserver:
	poetry run python -m core.manage runserver


.PHONY:huey
huey:
	poetry run python -m core.manage run_huey


.PHONY:superuser
superuser:
	poetry run python -m core.manage createsuperuser


.PHONY:setup
setup: install migrations migrate install-pre-commit ;


.PHONY:push-update
push-update: migrations migrate collectstatic ;


.PHONY:coverage-test
coverage-test:
	poetry run python -m core.manage test


.PHONY:coverage-report
coverage-report:
	poetry run coverage report


.PHONY:coverage-html
coverage:
	poetry run coverage html


.PHONY:run-coverage
run-coverage: coverage-test coverage-report coverage-html ;
