PYTHON="python3"

isort:
	isort .

mypy:
	mypy *.py setsolver/

flake8:
	flake8 .

black:
	black .

lint: isort mypy flake8 black

unit-test:
	${PYTHON} -m unittest

test: unit-test