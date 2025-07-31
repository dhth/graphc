from typing import Iterator

from prompt_toolkit.completion import (
    CompleteEvent,
    Completer,
    Completion,
    PathCompleter,
)
from prompt_toolkit.document import Document


class QueryFilePathCompleter(Completer):
    def __init__(self) -> None:
        self.path_completer = PathCompleter()

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterator[Completion]:
        text = document.text

        if text.startswith("@"):
            file_part = text[1:]

            file_document = Document(file_part, cursor_position=len(file_part))

            for completion in self.path_completer.get_completions(
                file_document, complete_event
            ):
                yield Completion(
                    text=completion.text,
                    start_position=completion.start_position,
                    display=completion.text,
                )
