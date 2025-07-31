from conftest import Runner
from inline_snapshot import snapshot

# ------------- #
#   SUCCESSES   #
# ------------- #


def test_help_flag(runner: Runner):
    # GIVEN
    args = ["--help"]
    env = {}

    # WHEN
    result = runner(args, env)

    # THEN
    assert result == snapshot("""\
success: true
exit_code: 0
----- stdout -----
usage: graphc [-h] [-q STRING] [-d STRING] [-b] [-n INTEGER] [-w INTEGER]
              [--debug]

Query Neo4j/Neptune databases

options:
  -h, --help            show this help message and exit
  -q STRING, --query STRING
                        Cypher query to execute. If not provided, starts
                        interactive mode.
  -d STRING, --db-uri STRING
                        Database URI
  -b, --benchmark       Benchmark query execution times without showing
                        results (only applicable in query mode)
  -n INTEGER, --bench-num-runs INTEGER
                        Number of benchmark runs (default: 5)
  -w INTEGER, --bench-warmup-num-runs INTEGER
                        Number of warmup runs before benchmarking (default: 0)
  --debug               Print runtime configuration and exit

examples:
  # Interactive mode
  DB_URI='bolt://127.0.0.1:7687' DB_USER='user' DB_PASSWORD='password' graphc
  graphc -d 'bolt://abc.xyz.us-east-1.neptune.amazonaws.com:8182'

  # One-off query mode
  graphc --query 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5'
  graphc -q - < query.cypher
  echo 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5' | graphc -q -
----- stderr -----
""")


def test_debug_flag(runner: Runner):
    # GIVEN
    args = [
        "--db-uri",
        "bolt://127.0.0.1:9999",
        "--query",
        "MATCH (n: Node) RETURN n.id, n.name LIMIT 5",
        "--benchmark",
        "--bench-num-runs",
        "10",
        "--bench-warmup-num-runs",
        "3",
        "--debug",
    ]
    env = {}

    # WHEN
    result = runner(args, env)

    # THEN
    assert result == snapshot("""\
success: true
exit_code: 0
----- stdout -----
debug info

database URI               bolt://127.0.0.1:9999
query                      MATCH (n: Node) RETURN n.id, n.name LIMIT 5
benchmark                  True
benchmark num runs         10
benchmark warmup num runs  3
----- stderr -----
""")


def test_db_uri_can_be_provided_via_an_env_var(runner: Runner):
    # GIVEN
    args = [
        "--debug",
    ]
    env = {
        "DB_URI": "bolt://127.0.0.1:9999",
    }

    # WHEN
    result = runner(args, env)

    # THEN
    assert result == snapshot("""\
success: true
exit_code: 0
----- stdout -----
debug info

database URI               bolt://127.0.0.1:9999
----- stderr -----
""")


# ------------ #
#   FAILURES   #
# ------------ #


def test_db_uri_is_mandatory(runner: Runner):
    # GIVEN
    args = ["--query", "MATCH (n: Node) RETURN n"]
    env = {"DB_URI": ""}

    # WHEN
    result = runner(args, env)

    # THEN
    assert result == snapshot("""\
success: false
exit_code: 1
----- stdout -----

----- stderr -----
Error: database URI is empty
""")


def test_benchmark_requires_query(runner: Runner):
    # GIVEN
    args = ["--benchmark"]
    env = {"DB_URI": "bolt://127.0.0.1:9999"}

    # WHEN
    result = runner(args, env)

    # THEN
    assert result == snapshot("""\
success: false
exit_code: 1
----- stdout -----

----- stderr -----
Error: benchmarking is only applicable in query mode
""")


def test_benchmark_num_runs_need_to_be_greater_than_one(runner: Runner):
    # GIVEN
    args = [
        "--query",
        "MATCH (n: Node) RETURN n",
        "--benchmark",
        "--bench-num-runs",
        "0",
    ]
    env = {}

    # WHEN
    result = runner(args, env)

    # THEN
    assert result == snapshot("""\
success: false
exit_code: 1
----- stdout -----

----- stderr -----
Error: number of benchmark runs must be >= 1
""")


def test_benchmark_warmup_num_runs_need_to_be_non_negative(runner: Runner):
    # GIVEN
    args = [
        "--query",
        "MATCH (n: Node) RETURN n",
        "--benchmark",
        "--bench-warmup-num-runs",
        "-1",
    ]
    env = {}

    # WHEN
    result = runner(args, env)

    # THEN
    assert result == snapshot("""\
success: false
exit_code: 1
----- stdout -----

----- stderr -----
Error: number of warmup runs must be >= 0
""")


def test_db_uri_requires_a_scheme(runner: Runner):
    # GIVEN
    args = []
    env = {"DB_URI": "127.0.0.1:9999"}

    # WHEN
    result = runner(args, env)

    # THEN
    assert result == snapshot("""\
success: false
exit_code: 1
----- stdout -----

----- stderr -----
Error: URI scheme '' is not supported. Supported URI schemes are ['bolt', \n\
'bolt+ssc', 'bolt+s', 'neo4j', 'neo4j+ssc', 'neo4j+s']. Examples: \n\
bolt://host[:port] or neo4j://host[:port][?routing_context]
""")


def test_db_uri_scheme_needs_to_be_supported(runner: Runner):
    # GIVEN
    args = []
    env = {"DB_URI": "blah://127.0.0.1:9999"}

    # WHEN
    result = runner(args, env)

    # THEN
    assert result == snapshot("""\
success: false
exit_code: 1
----- stdout -----

----- stderr -----
Error: URI scheme 'blah' is not supported. Supported URI schemes are ['bolt', \n\
'bolt+ssc', 'bolt+s', 'neo4j', 'neo4j+ssc', 'neo4j+s']. Examples: \n\
bolt://host[:port] or neo4j://host[:port][?routing_context]
""")
