PYTHON ?= python3
export PYTHONPATH := src

.PHONY: test
test:
	$(PYTHON) -m unittest discover -s tests -v
