from pathlib import Path
from typing import List

from prompt_toolkit.history import FileHistory


class QueryFileHistory(FileHistory):
    def __init__(self, filename: Path, *, strings_to_ignore: List[str]) -> None:
        super().__init__(filename)
        self._strings_to_ignore = set(strings_to_ignore)

    def append_string(self, string: str) -> None:
        for s in self._strings_to_ignore:
            if string.startswith(s):
                return

        super().append_string(string)
