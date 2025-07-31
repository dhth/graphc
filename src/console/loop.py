import os
from pathlib import Path
from typing import List

from neo4j import Driver
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from rich import print as rprint

from db import query_and_print_result

from .completions import QueryFilePathCompleter
from .utils import get_query_from_file

CLEAR_CMDS = ["clear"]
HELP_CMDS = ["help", ":h"]
QUIT_CMDS = ["bye", "exit", "quit", ":q"]


def run_loop(driver: Driver, db_uri: str, history_file_path: Path) -> None:
    print_banner()
    print_help(db_uri)
    loop(driver, db_uri, history_file_path)


def print_banner() -> None:
    rprint(r"""[blue]
                             __                
                            /\ \               
   __   _ __    __     _____\ \ \___     ___   
 /'_ `\/\`'__\/'__`\  /\ '__`\ \  _ `\  /'___\ 
/\ \L\ \ \ \//\ \L\.\_\ \ \L\ \ \ \ \ \/\ \__/ 
\ \____ \ \_\\ \__/.\_\\ \ ,__/\ \_\ \_\ \____\
 \/___L\ \/_/ \/__/\/_/ \ \ \/  \/_/\/_/\/____/
   /\____/               \ \_\                 
   \_/__/                 \/_/

[/blue]""")


def print_help(db_uri: str) -> None:
    help_text = f"""\
[blue]connected to {db_uri}[/]

[yellow]commands[/yellow]
[yellow]  '{"/".join(HELP_CMDS)}' to show help[/]
[yellow]  '{"/".join(CLEAR_CMDS)}' to clear screen[/]
[yellow]  '{"/".join(QUIT_CMDS)}' to quit[/]
[yellow]  '@<filename>' to execute query from a local file[/]

[green]keymaps[/green]
[green]  '<esc>' to enter vim mode[/]
[green]  '↑' to scroll up[/]
[green]  'k' to scroll up (in vim mode)[/]
[green]  '↓' to scroll down[/]
[green]  'j' to scroll down (in vim mode)[/]
[green]  'tab' to cycle through path suggestions (in insert mode, after '@')[/]
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


def loop(driver: Driver, db_uri: str, history_file_path: Path) -> None:
    history = QueryFileHistory(
        history_file_path, strings_to_ignore=HELP_CMDS + CLEAR_CMDS + QUIT_CMDS
    )

    completer = QueryFilePathCompleter()

    while True:
        user_input = prompt(
            ">> ",
            history=history,
            vi_mode=True,
            enable_history_search=True,
            completer=completer,
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

        query_to_run: str

        if user_input.startswith("@"):
            file_path = user_input[1:].strip()
            try:
                query_to_run = get_query_from_file(file_path)
            except Exception as e:
                rprint(f"[red]Error[/]: failed to read query from file: {e}")
                print()
                continue
        else:
            query_to_run = user_input

        try:
            query_and_print_result(driver, query_to_run)
        except Exception as e:
            rprint(f"[red]Error[/]: {e}")

        print()


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
