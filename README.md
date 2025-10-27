## Data science playground with the new Python stack

The [State of Python 2025](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025/) survey shows that **86% of respondents use Python** as their main language. Half of that use Python for data exploration and processing. This growth is in part driven by the Rust-revolution: many core data science libraries are being rewritten in Rust. To illustrate, as of September 2025, I have switched from

- `pandas` to `polars`
- `black` to `ruff`
- `pyenv` and `pip` to `uv`
- `pydantic v1` to `pydantic v2`
- `flask` to `FastAPI`
- `jupyter notebook` to `marimo`

The polars dataframe API has emerged as a de facto standard, as illustrated by the popularity of the [`narwhals`](https://github.com/narwhals-dev/narwhals) dataframe interoperability layer.

On top of that, in-memory analytical engines like [DuckDB](https://duckdb.org), [Kuzu](https://docs.kuzudb.com/) and [LanceDB](https://docs.kuzudb.com/) have made it a lot easier to use databases (relational, property graph or vector database, respectively) in the data engineering workflow.

So given all these developments, I am gradually rewriting my example notebooks in this new stack.

## Getting started

### Installing the playground on your local machine

- Install the basic commandline tools, if you haven't already done so:
    - [podman](https://podman-desktop.io)
    - [just](https://just.systems/man/en/prerequisites.html)
    - [uv](https://just.systems/man/en/prerequisites.html)
    - [git](https://github.com/git-guides/install-git)
- Clone this repo by running `git clone git@github.com:anthology-of-data-science/playground.git && cd playground && uv sync`

### Play with notebooks

- Ames Housing machine learning starter: `just ames-notebook`

### Play with cypher query language

- Loading data graph database: `just load-kuzu-database` (needs to be run at least once to create the local database)
- `just kuzu-explorer`