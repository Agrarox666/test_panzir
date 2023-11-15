lint:
	poetry run flake8 app
	poetry run flake8 project_tests

tests_no_bd:
	pytest -vv tests_modules/tests_no_bd.py

tests_bd:
	python project_tests/tests_bd.py

run_no_bd:
	python app_no_bd.py

run:
	python run.py

install:
	poetry install