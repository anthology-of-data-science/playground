## Data science with the new Python stack

The [State of Python 2025](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025/) survey shows that **86% of respondents use Python** as their main language. Half of that use Python for data erxploration and processing. This growth is in part driven by the Rust-revolution: many core data science libraries are being rewritten in Rust. To illustrate, as of September 2025, I have switched from

- `pandas` to `polars`
- `black` to `ruff`
- `pyenv` and `pip` to `uv`
- `pydantic v1` to `pydantic v2`
- `flask` to `FastAPI`

The polars dataframe API has emerged as a de facto standard, as illustrated by the popularity of the [`narwhals`](https://github.com/narwhals-dev/narwhals) dataframe interoperability layer.

So given all these developments, I am gradually rewriting my example notebooks in this new stack.