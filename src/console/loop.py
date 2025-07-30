import os
from pathlib import Path
from typing import List

from neo4j import Driver
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from rich import print as rprint

from db import query_and_print_result

CLEAR_CMDS = ["clear"]
HELP_CMDS = ["help", ":h"]
QUIT_CMDS = ["bye", "exit", "quit", ":q"]


def run_loop(driver: Driver, db_uri: str, history_file_path: Path):
    print_banner()
    print_help(db_uri)
    loop(driver, db_uri, history_file_path)


def print_banner():
    rprint(r"""[blue]
                     _    ___ 
  __ _ _ _ __ _ _ __| |_ / __|
 / _` | '_/ _` | '_ \ ' \ (__ 
 \__, |_| \__,_| .__/_||_\___|
 |___/         |_|
[/blue]""")


def print_help(db_uri: str):
    help_text = f"""\
[blue]connected to {db_uri}[/blue]

[yellow]commands[/yellow]
[yellow]  '{"/".join(HELP_CMDS)}' to show help[/yellow]
[yellow]  '{"/".join(CLEAR_CMDS)}' to clear screen[/yellow]
[yellow]  '{"/".join(QUIT_CMDS)}' to quit[/yellow]

[green]keymaps[/green]
[green]  '<esc>' to enter vim mode[/green]
[green]  '↑' to scroll up[/green]
[green]  'k' to scroll up (in vim mode)[/green]
[green]  '↓' to scroll down[/green]
[green]  'j' to scroll down (in vim mode)[/green]
"""
    rprint(help_text)


class QueryFileHistory(FileHistory):
    def __init__(self, filename: Path, *, strings_to_ignore: List[str]) -> None:
        super().__init__(filename)
        self._strings_to_ignore = set(strings_to_ignore)

    def append_string(self, string: str) -> None:
        if string in self._strings_to_ignore:
            return

        super().append_string(string)


def loop(driver: Driver, db_uri: str, history_file_path: Path):
    history = QueryFileHistory(
        history_file_path, strings_to_ignore=HELP_CMDS + CLEAR_CMDS + QUIT_CMDS
    )

    while True:
        user_input = prompt(
            ">> ",
            history=history,
            vi_mode=True,
            enable_history_search=True,
        ).strip()

        if user_input == "":
            continue

        if user_input in QUIT_CMDS:
            print("bye 👋")
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
            rprint(f"[red]Error[/red]: {e}")

        print()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
