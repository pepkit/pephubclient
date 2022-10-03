lint:
	black . && isort . && flake8

run-coverage:
	coverage run -m pytest

html-report:
	coverage html

open-coverage:
	cd htmlcov && google-chrome index.html

coverage: run-coverage html-report open-coverage
