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
usage: graphc [-h] [-q STRING] [-d STRING]

Query Neo4j/Neptune databases

options:
  -h, --help            show this help message and exit
  -q STRING, --query STRING
                        Cypher query to execute. If not provided, starts interactive mode.
  -d STRING, --db-uri STRING
                        Database URI
```

```bash
# Interactive mode
DB_URI='bolt://127.0.0.1:7687' DB_USER='user' DB_PASSWORD='password' graphc
graphc -d 'bolt://abc.xyz.us-east-1.neptune.amazonaws.com:8182'

# One-off query mode
graphc --query 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5'
echo 'MATCH (n: Node) RETURN n.id, n.name LIMIT 5' | graphc -q -
```
