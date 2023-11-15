lint:
	poetry run flake8 app
	poetry run flake8 project_tests

tests_no_db:
	poetry run pytest -vv project_tests/tests_no_db.py

tests_db:
	poetry run python project_tests/tests_db.py

run_no_db:
	poetry run python app_no_bd.py

run:
	poetry run python run.py

install:
	poetry install