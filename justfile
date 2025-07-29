set dotenv-load

alias f := format
alias t := ty
alias l := lint
alias q := query
alias r := run

format *FLAGS:
    ruff format . {{FLAGS}}

ruff *FLAGS:
    uv run ruff check . {{FLAGS}}

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
