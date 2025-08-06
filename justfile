set dotenv-load

alias f := format
alias i := install
alias l := lint
alias q := query
alias r := run
alias re := review
alias t := test

format *FLAGS:
    uv run ruff format . {{FLAGS}}
    uv run ruff check . --fix

ty *FLAGS:
    uv run ty check . {{FLAGS}}

lint:
    uv run ruff format --check .
    uv run ruff check .
    uv run ty check .

query query *FLAGS:
    uv run src/main.py --query '{{query}}' {{FLAGS}}

run *FLAGS:
    uv run src/main.py {{FLAGS}}

install:
    uv tool install --reinstall .

queryf FILE:
    uv run src/main.py -q - < {{FILE}}

test *FLAGS:
    uv run pytest -v --inline-snapshot report {{FLAGS}}

review *FLAGS:
    uv run pytest -v --inline-snapshot review {{FLAGS}}

[working-directory: 'dev']
dev-up:
    docker compose up -d

dev-load-data:
    just queryf dev/queries/01-people.cypher > /dev/null
    just queryf dev/queries/02-companies.cypher > /dev/null
    just queryf dev/queries/03-works-at.cypher > /dev/null

dev-query:
    just query "MATCH (p:Person)-[r:WORKS_AT]->(c:Company) RETURN p.name, r.role, c.name"

[working-directory: 'dev']
dev-down:
    docker compose down -v
