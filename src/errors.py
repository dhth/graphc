class UserDataDirError(Exception):
    pass


class StdinIsTTYError(Exception):
    pass


def is_error_unexpected(exc: Exception) -> bool:
    match exc:
        case UserDataDirError():
            return True
        case _:
            return False


def error_follow_up(exc: Exception) -> str | None:
    match exc:
        case StdinIsTTYError():
            return """\
Tip: Pass query via stdin as follows:
  echo 'MATCH (n) RETURN n LIMIT 5' | graphc -q -
  graphc -q - < query.cypher
  graphc -q - <<< 'MATCH (n) RETURN n LIMIT 5'\
"""
        case _:
            return None
