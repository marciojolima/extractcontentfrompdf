PYTEST = poetry run pytest

.PHONY: test coverage check

test:
	$(PYTEST)

coverage:
	$(PYTEST) --cov-report=term-missing --cov-report=html

check:
	$(PYTEST)
