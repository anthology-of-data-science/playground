import marimo

__generated_with = "0.16.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Working with Kuzu and networkx

    ## The MovieLens database

    - https://grouplens.org/datasets/movielens/
    """
    )
    return


@app.cell
def _():
    from dataclasses import dataclass
    from urllib.request import urlretrieve
    from pathlib import Path
    from zipfile import ZipFile

    import kuzu
    import marimo as mo
    import networkx as nx
    import polars as pl


    @dataclass
    class MovieLens:
        """Dataclass object to do all the file handling and setting up the demo."""

        base_url: str = "https://files.grouplens.org/datasets/movielens/"
        dataset: str = "ml-latest-small"
        data_path: Path = Path("./data/movielens")
        db_path: Path = data_path / "kuzu-movielens-db"

        @classmethod
        def get_data(cls):
            path, headers = urlretrieve(cls.base_url + cls.dataset + ".zip", cls.data_path / ".".join((cls.dataset, "zip")))
            with ZipFile(path, "r") as zip:
                zip.extractall(cls.data_path)

        @classmethod
        def load_data(cls):
            if cls.db_path.exists():
                cls.db_path.unlink()

            db = kuzu.Database(cls.db_path)
            conn = kuzu.Connection(db)

            for ddl in (
                "CREATE NODE TABLE Movies (movieId INT64, year INT64, title STRING, genres STRING, PRIMARY KEY (movieId))",
                "CREATE NODE TABLE Users (userId INT64, PRIMARY KEY (userId))",
                "CREATE REL TABLE Ratings (FROM Users TO Movies, rating DOUBLE, timestamp TIMESTAMP)",
                "CREATE REL TABLE Tags (FROM Users TO Movies, tag STRING, timestamp TIMESTAMP)",
            ):
                conn.execute(ddl)

            movies = pl.read_csv(MovieLens.data_path / "ml-latest-small/movies.csv").select(
                pl.col("movieId"),
                pl.col("title").str.extract(r"\((\d+)").cast(pl.Int32).alias("year"),
                pl.col("title").str.extract(r"^([^\(]*)"),
                pl.col("genres"),
            )
            conn.execute("COPY Movies from movies")

            users = pl.read_csv(cls.data_path / "ml-latest-small/ratings.csv").select(pl.col("userId").unique())
            conn.execute("COPY Users from users")

            ratings = pl.read_csv(MovieLens.data_path / "ml-latest-small/ratings.csv").select(
                pl.col("userId").alias("from"),
                pl.col("movieId").alias("to"),
                pl.col("rating"),
                (pl.col("timestamp") * 1_000).cast(pl.Datetime(time_unit="ms")),
            )
            conn.execute("COPY Ratings from ratings")

            tags = pl.read_csv(MovieLens.data_path / "ml-latest-small/tags.csv").select(
                pl.col("userId").alias("from"),
                pl.col("movieId").alias("to"),
                pl.col("tag"),
                (pl.col("timestamp") * 1_000).cast(pl.Datetime(time_unit="ms")),
            )
            conn.execute("COPY Tags from tags")
    return MovieLens, kuzu, mo, nx


@app.cell
def _(MovieLens):
    MovieLens.get_data()
    MovieLens.load_data()
    return


@app.cell
def _(MovieLens, kuzu):
    db = kuzu.Database(MovieLens.db_path)
    conn = kuzu.Connection(db)
    return (conn,)


@app.cell
def _(conn, nx):
    res = conn.execute('MATCH (u:Users)-[r:Ratings]->(m:Movies) RETURN u, r, m')
    G = res.get_as_networkx(directed=False)
    pageranks = nx.pagerank(G)
    return (pageranks,)


@app.cell
def _(pageranks):
    pageranks
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
