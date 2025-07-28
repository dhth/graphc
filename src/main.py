import os
import sys
import pandas as pd
from neo4j import GraphDatabase, Driver
from boto3 import Session
from utils.auth import NeptuneAuthToken
from domain.servicekind import NeptuneServiceKind
from rich import print
from cli import parse_args


def run_loop(driver: Driver):
    quit_prompts = [
        "bye",
        "exit",
        "quit",
    ]
    print(r"""[blue]
                     _    ___ 
  __ _ _ _ __ _ _ __| |_ / __|
 / _` | '_/ _` | '_ \ ' \ (__ 
 \__, |_| \__,_| .__/_||_\___|
 |___/         |_|
[/blue]""")
    server_info = driver.get_server_info()
    print(f"[blue]connected to {server_info.address}[/blue]")
    print("[yellow]Commands[/yellow]")
    print("[yellow]  - 'clear' to clear screen[/yellow]")
    print("[yellow]  - 'bye/exit/quit' to quit[/yellow]")
    print()

    while True:
        user_input = input(">> ").strip()
        if user_input in quit_prompts:
            return

        if user_input == "clear":
            clear_screen()
            continue

        try:
            query_and_print_result(driver, user_input)
        except Exception as e:
            print(f"[red]Error[/red]: {e}")

        print()


def query_and_print_result(driver: Driver, query: str):
    result = query_db(driver, query)
    if result.shape[0] == 0:
        print("[grey66]no data found[/grey66]")
    else:
        print(result)
        print(f"[orange1]{result.shape[0]} x {result.shape[1]}[/orange1]")


def get_db_driver() -> Driver:
    db_uri = os.environ["DB_URI"]

    if "neptune.amazonaws.com" in db_uri:
        session = Session()
        region = os.environ.get("AWS_REGION", "us-east-1")
        auth_token = NeptuneAuthToken(
            credentials=session.get_credentials(),
            region=region,
            url=db_uri,
            service=NeptuneServiceKind.DB,
        )

        return GraphDatabase.driver(db_uri, auth=auth_token, encrypted=True)
    else:
        user_name = os.environ.get("DB_USER", "neo4j")
        password = os.environ.get("DB_PASSWORD", "password")
        return GraphDatabase.driver(db_uri, auth=(user_name, password))


def query_db(driver: Driver, query: str) -> pd.DataFrame:
    with driver.session() as session:
        return session.run(query).to_df()  # type: ignore[arg-type]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    args = parse_args()

    driver = get_db_driver()
    driver.verify_connectivity()

    if args.query:
        query_and_print_result(driver, args.query)
    else:
        run_loop(driver)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[red]Error[/red]: {e}", file=sys.stderr)
