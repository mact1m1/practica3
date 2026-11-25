PYTHON ?= python3
export PYTHONPATH := src

.PHONY: test
test:
	$(PYTHON) -m unittest discover -s tests -v

.PHONY: demo
demo:
	mkdir -p build
	sh run.sh asm examples/spec.json build/spec.bin --test
	@set -e; for name in vector1 vector2 vector3; do \
		sh run.sh asm examples/$$name.json build/$$name.bin; \
		sh run.sh run build/$$name.bin build/$$name.csv --range 20 25; \
		diff -u examples/expected/$$name.csv build/$$name.csv; \
		echo "$$name"; cat build/$$name.csv; \
	done
