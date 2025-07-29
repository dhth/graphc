from neo4j import Driver
import pandas as pd
from rich import print


def query_and_print_result(driver: Driver, query: str):
    result = _query_db(driver, query)
    if result.empty:
        print("[grey66]no data found[/grey66]")
    else:
        print(result)
        print(f"[orange1]{result.shape[0]} x {result.shape[1]}[/orange1]")


def _query_db(driver: Driver, query: str) -> pd.DataFrame:
    with driver.session() as session:
        return session.run(query).to_df()  # type: ignore[arg-type]
