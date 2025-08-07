import os
import time
from copy import deepcopy
from pathlib import Path

from neo4j import Driver
from neo4j.exceptions import ServiceUnavailable
from prompt_toolkit import PromptSession
from rich import print as rprint

from db import query_and_print_result
from domain import OutputFormat, RunBehaviours

from .completions import QueryFilePathCompleter
from .history import QueryFileHistory
from .utils import get_query_from_file

CLEAR_CMD = "clear"
CONNECTION_CMD = "connection"
HELP_CMDS = ["help", ":h"]
WRITE_CMD = "write"
PRINT_CMD = "print"
QUIT_CMDS = ["bye", "exit", "quit", ":q"]

ON = "on"
OFF = "off"

CTRL_C_WINDOW_SECONDS = 2


class Console:
    def __init__(
        self,
        driver: Driver,
        db_uri: str,
        history_file_path: Path,
        behaviours: RunBehaviours,
    ) -> None:
        self.driver = driver
        self.db_uri = db_uri
        self.behaviours = deepcopy(behaviours)
        self.history = QueryFileHistory(
            history_file_path,
            strings_to_ignore=HELP_CMDS
            + [CLEAR_CMD]
            + [CONNECTION_CMD]
            + [WRITE_CMD]
            + [PRINT_CMD]
            + QUIT_CMDS,
        )
        self.completer = QueryFilePathCompleter()
        self.keep_looping = True
        self.last_ctrl_c_time = None
        self.prompt_session = PromptSession(
            history=self.history,
            vi_mode=True,
            enable_history_search=True,
            completer=self.completer,
        )

    def run(self) -> None:
        self._print_banner()
        rprint(f"""\
[blue]connected to {self.db_uri}[/]
""")
        self._print_help()
        self._loop()

    def _loop(self) -> None:
        while self.keep_looping:
            if self.behaviours.write:
                rprint(
                    f"[cyan]write mode ({self.behaviours.output_format.value}) is ON[/]"
                )
                rprint()

            try:
                user_input = self.prompt_session.prompt(">> ").strip()
            except KeyboardInterrupt as e:
                buffer_empty = self.prompt_session.app.current_buffer.text.strip() == ""

                # user had a query entered, cancel it and move on
                if not buffer_empty:
                    continue

                if (
                    self.last_ctrl_c_time is not None
                    and time.time() - self.last_ctrl_c_time < CTRL_C_WINDOW_SECONDS
                ):
                    # prompt was empty and user pressed ctrl+c within the quit window; quit
                    raise e
                else:
                    # prompt was empty and user pressed ctrl+c either the first
                    # time or after the quit window passed
                    rprint(
                        f"[grey50]Press Ctrl-C again within {CTRL_C_WINDOW_SECONDS} seconds to quit[/]"
                    )
                    self.last_ctrl_c_time = time.time()
                    continue

            if user_input == "":
                continue

            was_command = self._handle_command(user_input)
            if was_command:
                continue

            query: str
            if user_input.startswith("@"):
                try:
                    query = get_query_from_file(user_input[1:].strip())
                except Exception as e:
                    rprint(f"[red]Error[/]: failed to read query from file: {e}")
                    continue
            else:
                query = user_input

            self._handle_query(query)

    def _handle_command(self, user_input: str) -> bool:
        if user_input in QUIT_CMDS:
            print("bye 👋")
            self.keep_looping = False
            return True

        if user_input in HELP_CMDS:
            self._print_help()
            return True

        if user_input == CLEAR_CMD:
            clear_screen()
            return True

        if user_input == CONNECTION_CMD:
            self._handle_conn_check()
            return True

        if user_input.startswith(PRINT_CMD):
            self._handle_print(user_input)
            return True

        if user_input.startswith(WRITE_CMD):
            self._handle_write(user_input)
            return True

        return False

    def _handle_print(self, user_input: str) -> None:
        els = user_input.split()
        arg = els[1] if len(els) == 2 else None
        if not (arg == OFF or arg == ON):
            rprint(
                f"[red]Error[/]: incorrect command provided; correct syntax: 'print <on/off>'"
            )
            return

        if arg == OFF:
            self.behaviours.print_query = False
            rprint(f"[yellow]print mode turned OFF[/]")
        else:
            self.behaviours.print_query = True
            rprint(f"[yellow]print mode turned ON[/]")

    def _handle_write(self, user_input: str) -> None:
        els = user_input.split()
        if len(els) != 2:
            rprint(
                f"[red]Error[/]: incorrect command provided; correct syntax: 'write {'/'.join(OutputFormat.choices())}/off'"
            )
            return

        arg = els[1]
        if arg == OFF:
            self.behaviours.write = False
            rprint(f"[yellow]write mode turned OFF[/]")
            return

        try:
            new_output_format = OutputFormat.from_string(arg)
            self.behaviours.write = True
            self.behaviours.output_format = new_output_format
        except Exception as e:
            rprint(f"[red]Error[/]: {e}")

    def _handle_conn_check(self) -> None:
        try:
            self.driver.verify_connectivity()
            rprint(f"[green]connected to {self.db_uri}[/]")
        except ServiceUnavailable:
            rprint(f"[red]couldn't connect to {self.db_uri}[/]")
        except KeyboardInterrupt:
            rprint("[yellow]connection check cancelled[/]")
        except Exception as e:
            rprint(f"[red]Error[/]: {e}")

    def _handle_query(self, query: str) -> None:
        try:
            query_and_print_result(self.driver, query, self.behaviours)
            rprint(
                "\n[grey50]---------------------------------------------------------------\n"
            )

        except Exception as e:
            rprint(f"[red]Error[/]: {e}")

    def _print_banner(self) -> None:
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

    def _print_help(self) -> None:
        help_text = f"""\
[yellow]commands
  help / :h                      show help
  clear                          clear screen
  connection                     check connection status
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


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
