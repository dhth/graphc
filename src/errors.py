class UserDataDirError(Exception):
    pass


class StdinIsTTYError(Exception):
    pass


class AWSAuthError(Exception):
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
    elif isinstance(exc, AWSAuthError):
        return """\
Tip: You can provide authentication configuration for AWS via either of the following ways:

1. Using environment variables (https://docs.aws.amazon.com/sdkref/latest/guide/environment-variables.html)
  - Set the following environment variables with the appropriate values
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN

2. Using a profile contained in the shared AWS config (https://docs.aws.amazon.com/sdkref/latest/guide/file-format.html)
  - Ensure credentials for the profile to be used are refreshed
  - Set the following environment variables
    - AWS_PROFILE\
"""
    return None
