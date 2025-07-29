import os
from neo4j import Driver
from db import query_and_print_result
from rich import print

CLEAR_CMDS = ["clear"]
QUIT_CMDS = ["bye", "exit", "quit", ":q"]
HELP_CMDS = ["help", ":h"]


def run_loop(driver: Driver, db_uri: str):
    print_banner()
    print_help(db_uri)
    loop(driver, db_uri)


def loop(driver: Driver, db_uri: str):
    while True:
        user_input = input(">> ").strip()
        if user_input in QUIT_CMDS:
            return

        if user_input in HELP_CMDS:
            print_help(db_uri)
            continue

        if user_input in CLEAR_CMDS:
            clear_screen()
            continue

        try:
            query_and_print_result(driver, user_input)
        except Exception as e:
            print(f"[red]Error[/red]: {e}")

        print()


def print_banner():
    print(r"""[blue]
                     _    ___ 
  __ _ _ _ __ _ _ __| |_ / __|
 / _` | '_/ _` | '_ \ ' \ (__ 
 \__, |_| \__,_| .__/_||_\___|
 |___/         |_|
[/blue]""")


def print_help(db_uri: str):
    print(f"[blue]connected to {db_uri}[/blue]")
    print()
    print("[yellow]commands[/yellow]")
    print(f"[yellow]  - '{'/'.join(HELP_CMDS)}' to show help[/yellow]")
    print(f"[yellow]  - '{'/'.join(CLEAR_CMDS)}' to clear screen[/yellow]")
    print(f"[yellow]  - '{'/'.join(QUIT_CMDS)}' to quit[/yellow]")
    print()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
