PYTHON="python3"

isort:
	isort .

mypy:
	mypy *.py setsolver/

black:
	black .

pylint:
	pylint *.py setsolver/

flake8:
	flake8 .

lint: isort mypy black pylint flake8

unit-test:
	${PYTHON} -m unittest

test: unit-test