test:
	python -m pytest --pyargs --doctest-modules majerus

test-coverage:
	python -m pytest --pyargs --doctest-modules --cov=majerus --cov-report term majerus

test-coverage-html:
	python -m pytest --pyargs --doctest-modules --cov=majerus --cov-report html majerus
