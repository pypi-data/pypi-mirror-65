all:test pylint flake8 coverage

init:
	pipenv install --dev --ignore-pipfile

test:
	pipenv run py.test

pylint:
	pipenv run pylint kpd --output-format=colorized --reports=no

flake8:
	pipenv run flake8

coverage:
	pipenv run py.test --cov=kpd --cov-report xml --cov-report term --cov-report html
