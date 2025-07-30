import statistics
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


def benchmark_query(driver: Driver, query: str, num_runs: int, warmup_runs: int):
    if warmup_runs > 0:
        print(f"[bold yellow]Warming up ({warmup_runs} runs) ...[/]")
        for run in range(1, warmup_runs + 1):
            start = time.perf_counter()
            query_db(driver, query)
            took_ms = (time.perf_counter() - start) * 1000
            print(f"Warmup {run:2d}: {took_ms:8.2f} ms")
        print()

    print(f"[bold yellow]Benchmarking ({num_runs} runs) ...[/]")

    execution_times = []

    for run in range(1, num_runs + 1):
        start = time.perf_counter()
        query_db(driver, query)
        took_ms = (time.perf_counter() - start) * 1000
        execution_times.append(took_ms)

        print(f"Run {run:2d}: {took_ms:8.2f} ms")

    print(f"""
[bold yellow]Statistics:[/]
Mean:   {statistics.mean(execution_times):8.2f} ms
Median: {statistics.median(execution_times):8.2f} ms
Min:    {min(execution_times):8.2f} ms
Max:    {max(execution_times):8.2f} ms\
""")
