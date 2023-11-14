lint:
	flake8 app.py
	flake8 tests.py

tests:
	pytest -vv tests.py