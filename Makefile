lint:
	# black should be last in the list, as it lint the code. Tests can fail if order will be different
	flake8 && isort . && black .

run-coverage:
	coverage run -m pytest

html-report:
	coverage html

open-coverage:
	cd htmlcov && google-chrome index.html

coverage: run-coverage html-report open-coverage
