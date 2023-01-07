.PHONY: install format

install:
	@poetry install

format:
	isort .
	blue .
