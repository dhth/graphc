import argparse
from dataclasses import dataclass


@dataclass
class Args:
    query: str | None
    db_uri: str | None


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        description="Query Neo4j/Neptune databases",
        prog="graphc",
        epilog="""\
examples:
  # Interactive mode
  DB_URI='bolt://127.0.0.1:7687' DB_USER='user' DB_PASSWORD='password' graphc
  graphc -d 'bolt://abc.xyz.us-east-1.neptune.amazonaws.com:8182'

  # One-off query mode
  graphc --query 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5'
  echo 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5' | graphc -q -
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-q",
        "--query",
        type=str,
        metavar="STRING",
        help="Cypher query to execute. If not provided, starts interactive mode.",
    )

    parser.add_argument(
        "-d",
        "--db-uri",
        type=str,
        metavar="STRING",
        help="Database URI",
    )

    args = parser.parse_args()
    return Args(query=args.query, db_uri=args.db_uri)
