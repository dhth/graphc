import os
import sys
from pathlib import Path

from rich import print

import errors
from cli import parse_args
from console import run_loop
from db import get_db_driver, query_and_print_result
from utils import get_data_dir

AUTHOR = "@dhth"
ISSUES_URL = "https://github.com/dhth/graphc/issues"


def main():
    args = parse_args()

    db_uri = get_db_uri()
    driver = get_db_driver(db_uri)
    driver.verify_connectivity()

    if args.query:
        query_and_print_result(driver, args.query)
    else:
        user_data_dir = get_data_dir()
        history_file_path = Path(user_data_dir) / "history.txt"
        run_loop(driver, db_uri, history_file_path)


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
    except (EOFError, KeyboardInterrupt):
        pass
    except errors.UserDataDirError as e:
        print(f"[red]Error[/red]: {e}", file=sys.stderr)
        print("---")
        print(
            f"This isn't supposed to happen; let {AUTHOR} know via {ISSUES_URL}",
            file=sys.stderr,
        )
    except Exception as e:
        print(f"[red]Error[/red]: {e}", file=sys.stderr)
