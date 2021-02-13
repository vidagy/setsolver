PYTHON="./venv/bin/python3"
BIN="./venv/bin"

isort:
	${BIN}/isort .

mypy:
	${BIN}/mypy --strict *.py setsolver/

flake8:
	${BIN}/flake8 --exclude ./venv/ .

black:
	${BIN}/black . -l 79

lint: isort mypy flake8 black
