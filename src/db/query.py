import time

import pandas as pd
from neo4j import Driver
from rich import print


def query_and_print_result(driver: Driver, query: str, *, print_query: bool = False):
    start = time.perf_counter()
    result = query_db(driver, query)
    took_ms = (time.perf_counter() - start) * 1000

    if print_query:
        print(f"[yellow]---\n{query}\n---[/]")

    print()
    if result.empty:
        print("[grey66]no data found[/]")
    else:
        print(result)

    print(f"[grey66]Took {took_ms:.2f} ms")


def query_db(driver: Driver, query: str) -> pd.DataFrame:
    with driver.session() as session:
        return session.run(query).to_df()  # type: ignore[arg-type]
