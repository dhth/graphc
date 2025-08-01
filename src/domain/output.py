from enum import Enum


class OutputFormat(Enum):
    JSON = "json"
    CSV = "csv"

    @classmethod
    def choices(cls) -> list[str]:
        return [fmt.value for fmt in cls]

    @classmethod
    def default(cls) -> "OutputFormat":
        return cls.CSV

    @classmethod
    def from_string(cls, value: str) -> "OutputFormat":
        try:
            return cls(value.lower())
        except ValueError:
            valid_choices = ", ".join(cls.choices())
            raise ValueError(
                f"invalid output format '{value}'; valid choices: {valid_choices}"
            )
