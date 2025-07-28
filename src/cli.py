import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query Neo4j/Neptune databases", prog="neptunesh"
    )

    parser.add_argument(
        "--query",
        type=str,
        help="Cypher query to execute. If not provided, starts interactive mode.",
    )

    return parser.parse_args()
