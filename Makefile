.PHONY: validate test check

validate:
	python scripts/validate_governance.py

test:
	python -m unittest discover -s tests -v

check: validate test
	git diff --check
