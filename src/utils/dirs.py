from platformdirs import user_data_dir

from errors import UserDataDirError


def get_data_dir() -> str:
    try:
        return user_data_dir("graphc", ensure_exists=True)
    except Exception as e:
        raise UserDataDirError(f"couldn't get user data directory: {e}") from e
