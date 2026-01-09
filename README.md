## Data science with the new Python stack

The [State of Python 2025](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025/) survey shows that **86% of respondents use Python** as their main language. Half of that use Python for data exploration and processing. This growth is in part driven by the Rust-revolution: many core data science libraries are being rewritten in Rust. To illustrate, as of September 2025, I have switched from

- `jupyter` to `marimo` for notebooks
- `pandas` to `polars` for dataframes
- `black` to `ruff` for linting
- `pyenv` and `pip` to `uv` for package management
- `pydantic v1` to `pydantic v2` for data validation
- `flask` to `FastAPI` for APIs
- `autogluon` and Claude Code-assisted coding for machine learning

The polars dataframe API has emerged as a de facto standard, as illustrated by the popularity of the [`narwhals`](https://github.com/narwhals-dev/narwhals) dataframe interoperability layer.

On top of that, in-memory analytical engines like [DuckDB](https://duckdb.org), [Kuzu](https://docs.kuzudb.com/) and [LanceDB](https://docs.kuzudb.com/) have made it a lot easier to use databases (relational, property graph or vector database, respectively) in the data engineering workflow.

So given all these developments, I am gradually rewriting my example notebooks in this new stack.

## marimo as the new reactive notebook

- [WASM-powered HTML](https://docs.marimo.io/guides/publishing/github_pages/#export-to-wasm-powered-html)
