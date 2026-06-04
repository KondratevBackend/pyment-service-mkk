black_formatter:
	black ./src/ --config pyproject.toml

black_check:
	black ./src/ --config pyproject.toml --check

isort_formatter:
	isort . --settings-path pyproject.toml

isort_check:
	isort check . --settings-path pyproject.toml

ruff_checker:
	ruff check . --config pyproject.toml

run_formatters: black_formatter isort_formatter

run_linters: black_check isort_check ruff_checker
