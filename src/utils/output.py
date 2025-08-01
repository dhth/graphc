from datetime import datetime
from pathlib import Path

import pandas as pd

from domain import OutputFormat


def write_df(df: pd.DataFrame, format: OutputFormat) -> Path:
    output_path = get_output_path(format)
    write_df_to_file(df, format, output_path)

    return output_path


def get_output_path(format: OutputFormat) -> Path:
    output_dir = Path.cwd() / ".graphc"
    output_dir.mkdir(exist_ok=True)

    now = datetime.now()
    timestamp = now.strftime("%Y-%b-%d-%H-%M-%S").lower()

    match format:
        case OutputFormat.JSON:
            filename = f"{timestamp}.json"
        case OutputFormat.CSV:
            filename = f"{timestamp}.csv"

    return output_dir / filename


def write_df_to_file(df: pd.DataFrame, format: OutputFormat, file_path: Path):
    match format:
        case OutputFormat.JSON:
            df.to_json(file_path, index=False)
        case OutputFormat.CSV:
            df.to_csv(file_path, index=False)
