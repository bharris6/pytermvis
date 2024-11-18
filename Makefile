VENV           = .venv
BIN            = $(VENV)/bin
PY             = $(or $(shell which python3), $(shell which python))

default: all

$(VENV): pyproject.toml
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip pip-tools build bandit ruff pytest coverage
	$(BIN)/python -m piptools compile --generate-hashes pyproject.toml --output-file requirements.txt
	$(BIN)/pip install --only-binary :all: -r requirements.txt
	$(BIN)/pip install -e .
	touch $(VENV)

.PHONY: lint
lint: $(VENV)
	$(BIN)/python -m ruff check ./pytermvis/

.PHONY: scan
scan: $(VENV)
	$(BIN)/python -m bandit -r ./pytermvis/

.PHONY: test
test: $(VENV)
	$(BIN)/python -m coverage run --source=./pytermvis/ -m pytest test/
	$(BIN)/python -m coverage report -m

.PHONY: build
build: $(VENV) lint scan test
	$(BIN)/python -m build  .

.PHONY: install
install: $(VENV) build
	echo "Copy the built binary over to /usr/bin or something"

clean:
	rm -rf $(VENV) ./build ./dist ./*.egg-info ./.ruff_cache ./test/.pytest_cache
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

all: $(VENV) lint scan test
