from pathlib import Path

import pytest
from inline_snapshot import snapshot

from console.utils import get_query_from_file

TESTDATA_DIR = Path(__file__).parent / "testdata"

# ------------- #
#   SUCCESSES   #
# ------------- #


class TestGetQueryFromFile:
    def test_works_for_valid_file(self):
        # GIVEN
        query_file = TESTDATA_DIR / "simple.cypher"

        # WHEN
        result = get_query_from_file(str(query_file))

        # THEN
        assert result == snapshot("MATCH (n) RETURN n")

    def test_works_for_file_with_whitespace(self):
        # GIVEN
        query_file = TESTDATA_DIR / "whitespace.cypher"

        # WHEN
        result = get_query_from_file(str(query_file))

        # THEN
        assert result == snapshot("MATCH (n) RETURN n")

    def test_works_for_multiline_file(self):
        # GIVEN
        query_file = TESTDATA_DIR / "multiline.cypher"

        # WHEN
        result = get_query_from_file(str(query_file))

        # THEN
        assert result == snapshot("""\
MATCH (n:Person)
WHERE n.age > 25
RETURN n.name, n.age
ORDER BY n.age DESC\
""")

    # ------------ #
    #   FAILURES   #
    # ------------ #

    def test_fails_if_empty_string_provided(self):
        with pytest.raises(ValueError, match="no file specified"):
            get_query_from_file("")

    def test_fails_if_only_whitespace_provided(self):
        with pytest.raises(ValueError, match="no file specified"):
            get_query_from_file("   ")

    def test_fails_if_file_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            get_query_from_file("nonexistent_file.cypher")

    def test_fails_if_file_is_empty(self):
        # GIVEN
        empty_file = TESTDATA_DIR / "empty.cypher"

        # WHEN
        # THEN
        with pytest.raises(ValueError, match="file is empty"):
            get_query_from_file(str(empty_file))

    def test_fails_if_file_contains_only_whitespace(self):
        # GIVEN
        whitespace_file = TESTDATA_DIR / "whitespace-only.cypher"

        # WHEN
        # THEN
        with pytest.raises(ValueError, match="file is empty"):
            get_query_from_file(str(whitespace_file))
