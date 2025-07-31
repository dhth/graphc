from pathlib import Path


def get_query_from_file(file_path: str) -> str:
    if len(file_path.strip()) == 0:
        raise ValueError("no file specified")

    query_from_file = Path(file_path).read_text().strip()
    if not query_from_file:
        raise ValueError("file is empty")

    return query_from_file
