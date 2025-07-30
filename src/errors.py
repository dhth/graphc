class UserDataDirError(Exception):
    pass


class StdinIsTTYError(Exception):
    pass


def is_error_unexpected(exc: Exception) -> bool:
    return isinstance(exc, UserDataDirError)


def error_follow_up(exc: Exception) -> str | None:
    if isinstance(exc, StdinIsTTYError):
        return """\
Tip: Pass query via stdin as follows:
  echo 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5' | graphc -q -
  graphc -q - < query.cypher
  graphc -q - <<< 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5'\
"""
    return None
