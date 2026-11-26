PY ?= python

.PHONY: api-lint api-typecheck api-test api-build web-lint web-typecheck web-test web-build infra-typecheck infra-synth check-lab-imports check-docs check-migrations gate all

PHASE ?= 0
api-lint api-typecheck api-test api-build:
	$(PY) scripts/dev.py api $(patsubst api-%,%,$@)

web-lint web-typecheck web-test web-build:
	$(PY) scripts/dev.py web $(patsubst web-%,%,$@)

infra-typecheck infra-synth:
	$(PY) scripts/dev.py infra $(patsubst infra-%,%,$@)

check-lab-imports check-docs check-migrations:
	$(PY) scripts/dev.py check $(patsubst check-%,%,$@)

# Phase gate (R78): manual, not part of `all` or CI. Usage: make gate PHASE=0
gate:
	$(PY) scripts/dev.py gate --phase $(PHASE)

all:
	$(PY) scripts/dev.py all
