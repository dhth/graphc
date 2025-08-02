import os
from copy import deepcopy
from pathlib import Path
from typing import List

from neo4j import Driver
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from rich import print as rprint

from db import query_and_print_result
from domain import OutputFormat, RunBehaviours

from .completions import QueryFilePathCompleter
from .utils import get_query_from_file

CLEAR_CMD = "clear"
HELP_CMDS = ["help", ":h"]
WRITE_CMD = "write"
PRINT_CMD = "print"
QUIT_CMDS = ["bye", "exit", "quit", ":q"]

ON = "on"
OFF = "off"


def run_loop(
    driver: Driver, db_uri: str, history_file_path: Path, behaviours: RunBehaviours
) -> None:
    print_banner()
    print_help(db_uri)
    loop(driver, db_uri, history_file_path, behaviours)


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

[yellow]commands
  help / :h                      show help
  clear                          clear screen
  quit / exit / bye / :q         quit
  write <FORMAT>                 turn ON "write results" mode
  write off                      turn OFF "write results" mode
  @<filename>                    execute query from a local file
  print <on/off>                 toggle "print query" mode[/]

[green]keymaps
  <esc>                          enter vim mode
  ↑ / k                          scroll up in query history
  ↓ / j                          scroll down in query history
  tab                            cycle through path suggestions (in insert mode, after '@')[/]
"""
    rprint(help_text)


class QueryFileHistory(FileHistory):
    def __init__(self, filename: Path, *, strings_to_ignore: List[str]) -> None:
        super().__init__(filename)
        self._strings_to_ignore = set(strings_to_ignore)

    def append_string(self, string: str) -> None:
        for s in self._strings_to_ignore:
            if string.startswith(s):
                return

        super().append_string(string)


def loop(
    driver: Driver, db_uri: str, history_file_path: Path, behaviours: RunBehaviours
) -> None:
    history = QueryFileHistory(
        history_file_path,
        strings_to_ignore=HELP_CMDS
        + [CLEAR_CMD]
        + [WRITE_CMD]
        + [PRINT_CMD]
        + QUIT_CMDS,
    )

    loop_behaviours = deepcopy(behaviours)

    completer = QueryFilePathCompleter()

    just_cleared = False

    while True:
        if just_cleared:
            just_cleared = False

        if loop_behaviours.write:
            rprint(f"[cyan]write mode ({loop_behaviours.output_format.value}) is ON[/]")
            rprint()

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

        if user_input == CLEAR_CMD:
            clear_screen()
            just_cleared = True
            continue

        if user_input.startswith(PRINT_CMD):
            els = user_input.split()
            arg = els[1] if len(els) == 2 else None
            if not (arg == OFF or arg == ON):
                rprint(
                    f"[red]Error[/]: incorrect command provided; correct syntax: 'print <on/off>'"
                )
                continue

            if arg == OFF:
                loop_behaviours.print_query = False
                rprint(f"[yellow]print mode turned OFF[/]")
            else:
                loop_behaviours.print_query = True
                rprint(f"[yellow]print mode turned ON[/]")

            continue

        if user_input.startswith(WRITE_CMD):
            els = user_input.split()
            if len(els) != 2:
                rprint(
                    f"[red]Error[/]: incorrect command provided; correct syntax: 'write {'/'.join(OutputFormat.choices())}/off'"
                )
                continue

            arg = els[1]
            if arg == OFF:
                loop_behaviours.write = False
                rprint(f"[yellow]write mode turned OFF[/]")
                continue

            try:
                new_output_format = OutputFormat.from_string(arg)
                loop_behaviours.write = True
                loop_behaviours.output_format = new_output_format
            except Exception as e:
                rprint(f"[red]Error[/]: {e}")

            continue

        query_to_run: str

        if user_input.startswith("@"):
            file_path = user_input[1:].strip()
            try:
                query_to_run = get_query_from_file(file_path)
            except Exception as e:
                rprint(f"[red]Error[/]: failed to read query from file: {e}")
                continue
        else:
            query_to_run = user_input

        try:
            query_and_print_result(driver, query_to_run, loop_behaviours)
            rprint(
                "\n[grey50]---------------------------------------------------------------\n"
            )

        except Exception as e:
            rprint(f"[red]Error[/]: {e}")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
