# Directories that might be created during testing
TESTING_DIRS := .tox .eggs .cache .pytest_cache build dist htmlcov src/pyhibp.egg-info

# Likewise for files
TESTING_FILES := .coverage .pipenv-made Pipfile.lock .pytest-junit.xml

build:
	pipenv run python setup.py sdist bdist_wheel

# Create a target to create a pipenv once, then we can reuse it.
# ``pipenv run python setup.py develop;`` because otherwise Pipenv wants to glitch out and not actually install.
.PHONY: create-pipenv
create-pipenv:
	@if [ ! -f .pipenv-made ]; then \
		echo "Setting up the pipenv..."; \
		pipenv run python setup.py develop > /dev/null; \
		pipenv install --dev; \
		touch .pipenv-made; \
	fi

.PHONY: clean
clean:
	find . -type f -name '*.py[co]' -delete

.PHONY: dist-clean
dist-clean: clean
	- pipenv --rm
	- rm $(TESTING_FILES)
	- rm -r $(TESTING_DIRS)

.PHONY: dev
dev: create-pipenv

.PHONY: test
test: create-pipenv
	pipenv run pytest

.PHONY: test-cov
test-cov: create-pipenv
	pipenv run pytest --cov=pyhibp test/

.PHONY: check
check: create-pipenv
	pipenv run flake8

# The tox target can skip the pipenv creation (it gets setup during the run)
.PHONY: tox
tox: create-pipenv
	pipenv install tox --dev
	pipenv run tox
