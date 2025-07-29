import os
import sys

from rich import print

from cli import parse_args
from console import run_loop
from db import get_db_driver, query_and_print_result


def main():
    args = parse_args()

    db_uri = get_db_uri()
    driver = get_db_driver(db_uri)
    driver.verify_connectivity()

    if args.query:
        query_and_print_result(driver, args.query)
    else:
        run_loop(driver, db_uri)


def get_db_uri() -> str:
    db_uri = os.environ.get("DB_URI")
    if db_uri is None:
        raise ValueError("DB_URI is not set")

    db_uri = db_uri.strip()
    if db_uri == "":
        raise ValueError("DB_URI is empty")

    return db_uri


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[red]Error[/red]: {e}", file=sys.stderr)
