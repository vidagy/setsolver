PYTHON="python3"

isort:
	isort .

mypy:
	mypy --strict *.py setsolver/

flake8:
	flake8 --exclude ./venv/ .

black:
	black . -l 79

lint: isort mypy flake8 black

unit-test:
	${PYTHON} -m unittest test

test: unit-test