<p align="center">
  <h1 align="center">graphc</h1>
  <p align="center">
    <a href="https://github.com/dhth/graphc/actions/workflows/main.yml"><img alt="Build status" src="https://img.shields.io/github/actions/workflow/status/dhth/graphc/main.yml?style=flat-square"></a>
  </p>
</p>

`graphc` (stands for "graph console") lets you query Neo4j/AWS Neptune databases
via an interactive console.

> [!NOTE]
> graphc is work-in-progress software. Its interface and functionality is likely
> to change in the future.

⚡️ Usage
---

```text
usage: graphc [OPTIONS]

Query Neo4j/AWS Neptune databases via an interactive console

options:
  -h, --help            show this help message and exit
  -q STRING, --query STRING
                        Cypher query to execute. If not provided, starts interactive console
  -d STRING, --db-uri STRING
                        Database URI
  -b, --benchmark       Benchmark query execution times without showing results (only applicable in query mode)
  -n INTEGER, --bench-num-runs INTEGER
                        Number of benchmark runs (default: 5)
  -w INTEGER, --bench-warmup-num-runs INTEGER
                        Number of warmup runs before benchmarking (default: 0)
```

```bash
# Interactive mode
DB_URI='bolt://127.0.0.1:7687' DB_USER='user' DB_PASSWORD='password' graphc
graphc -d 'bolt://abc.xyz.us-east-1.neptune.amazonaws.com:8182'

# One-off query mode
graphc --query 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5'
graphc -q - < query.cypher
echo 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5' | graphc -q -
```

📟 Console
---

`graphc` comes with a console where you can execute queries in an interactive
manner.

![banner](https://tools.dhruvs.space/images/graphc/v0-1-0/banner.png)

### commands

- `help/:h` to show help
- `clear` to clear screen
- `bye/exit/quit/:q` to quit
- `@<filename>` to execute query from a local file

### Keymaps

- `<esc>` to enter vim mode
- `↑` to scroll up
- `k` to scroll up (in vim mode)
- `↓` to scroll down
- `j` to scroll down (in vim mode)
- `tab` to cycle through path suggestions (in insert mode, after `@`)

🔢 Benchmarking
---

You can benchmark the execution times for a query using the `--benchmark/-b`
flag.

```bash
cat query.cypher | graphc -c - -b -n 5 -w 2
```

```text
Warming up (2 runs) ...
Warmup  1:   627.84 ms
Warmup  2:   452.06 ms

Benchmarking (5 runs) ...
Run  1:   451.92 ms
Run  2:   449.51 ms
Run  3:   451.52 ms
Run  4:   453.09 ms
Run  5:   445.73 ms

Statistics:
Mean:     450.35 ms
Median:   451.52 ms
Min:      445.73 ms
Max:      453.09 ms
```
