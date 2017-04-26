test:
	python -m unittest discover

flake8:
	flake8 --ignore-dir=venv .

trial:
	python mutate.py test_example example example.py