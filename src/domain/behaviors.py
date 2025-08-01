from dataclasses import dataclass

from .output import OutputFormat


@dataclass
class RunBehaviours:
    write: bool
    output_format: OutputFormat
    print_query: bool
