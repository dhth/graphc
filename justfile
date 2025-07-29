set dotenv-load

alias f := format
alias t := ty
alias l := lint
alias q := query
alias r := run
alias i := install

format *FLAGS:
    uv run ruff format . {{FLAGS}}

ruff:
    uv run ruff check . --fix

ty *FLAGS:
    uv run ty check . {{FLAGS}}

lint:
    uv run ruff format --check .
    uv run ruff check .
    uv run ty check .

query query *FLAGS:
    uv run main.py --query '{{query}}' {{FLAGS}}

run *FLAGS:
    uv run src/main.py {{FLAGS}}

install:
    uv tool install .
