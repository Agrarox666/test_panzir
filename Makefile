lint:
	poetry run flake8 app
	poetry run flake8 project_tests

tests_no_bd:
	poetry run pytest -vv project_tests/tests_no_bd.py

tests_bd:
	poetry run python project_tests/tests_bd.py

run_no_bd:
	poetry run python app_no_bd.py

run:
	poetry run python run.py

install:
	poetry install