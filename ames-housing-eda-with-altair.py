import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from pprint import pp

    import altair as alt
    import marimo as mo
    import polars as pl
    import polars.selectors as cs
    return alt, cs, mo, pl, pp


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""This notebook demonstrates explorative data analysis using the [Ames Housing dataset ](https://github.com/EAISI/discover-projects/tree/main/ames-housing). To do so, it explores some of Altair's interesting features based on [this blogpost](https://www.kaggle.com/code/jacoporepossi/eda-is-awesome-having-fun-with-altair/notebook) and demonstrates some Python Kung Fu that is useful in day-to-day data wrangling."""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Load the dataset

    ## Do renaming and type casting when loading data
    """
    )
    return


@app.cell
def _(cs, pl):
    # url
    ames_data = "https://github.com/eaisi/discover-projects/blob/main/ames-housing/AmesHousing.csv?raw=true"

    # load and remove spaces in col names and cast types
    # use polars selectors https://docs.pola.rs/api/python/stable/reference/selectors.html
    df = (
        pl.read_csv(ames_data)
        .rename(lambda s: s.replace(" ", ""))
        .with_columns((cs.string() - cs.by_name(["Neighborhood"])).cast(pl.Categorical), pl.col("SalePrice").cast(pl.Int32))
    )

    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Join and download extra data directly""")
    return


@app.cell
def _(df, pl):
    # load names of neighbourhodds
    ames_names = "https://github.com/EAISI/discover-projects/raw/refs/heads/main/ames-housing/Neighborhood%20names.xlsx"


    def get_binary(url):
        """Download binary file in memory without saving to disk."""
        from io import BytesIO
        import requests

        try:
            response = requests.get(url)

            # Raise an exception if the request was unsuccessful (e.g., 404 Not Found)
            response.raise_for_status()

            # Get the binary content of the response
            file_content = response.content

            # Create an in-memory binary stream from the file content using BytesIO
            # This allows polars to read the data as if it were a file on disk
            file_buffer = BytesIO(file_content)

            # Read the Excel data from the buffer into a Polars DataFrame
            # The `read_excel` function can accept a file path or a file-like object
            df = pl.read_excel(file_buffer)

            return df

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during download: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
            return None


    df.join(get_binary(ames_names), on="Neighborhood", how="left").select(["PID", "Neighborhood", "Neighborhood_full"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Descriptive statistics

    Let start with some basics in polars


    """
    )
    return


@app.cell
def _(df, pp):
    # use schema attribute to get list of column names with types
    pp(df.schema)
    return


@app.cell
def _(cs, df):
    df.select(cs.numeric()).describe().with_columns(cs.numeric().round(2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Counting column types with `Counter`""")
    return


@app.cell
def _(df):
    # Count column dtypes
    from collections import Counter

    Counter(df.dtypes)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Count missing value per column""")
    return


@app.cell
def _(alt, df, pl):
    # list of columns with count of missing value in long format
    missing = (
        df.select(pl.all().is_null().sum())
        .transpose(include_header=True, column_names=["is_null_count"])
        .sort(by="is_null_count", descending=True)
    )

    # highlighted bar chart
    alt.Chart(missing.filter(pl.col("is_null_count") > 0)).mark_bar().encode(
        x="is_null_count",
        y=alt.X("column", sort="-x"),
        color=alt.condition(
            alt.datum["is_null_count"] > 10,  # If count missing is > 10%, returns True,
            alt.value("orange"),  # which sets the bar orange.
            alt.value("steelblue"),  # And if it's not true it sets the bar steelblue.
        ),
        tooltip=["is_null_count"],
    ).properties(width=500, height=300).configure_axis(grid=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Charts

    1. [Bar Chart with Highlighted Bar](#Bar-Chart-with-Highlighted-Bar)  
    2. [Boxplot](#Boxplot)  
    3. [Heatmaps](#Heatmaps)   
    4. [Bindings, Selections & Conditions](#Bindings,-Selections-&-Conditions)   
    5. [Interactive Chart with Cross-Highlight](#Interactive-Chart-with-Cross-Highlight)   
    6. [Dot Dash Plot](#Dot-Dash-Plot)  
    7. [Multifeature Scatter Plot](#Multifeature-Scatter-Plot)
    8. [Scatter Matrix](#Scatter-Matrix)
    9. [Layered Histogram](#Layered-Histogram)
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Bar Chart with Highlighted Bar""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Basic bar chart with a **bars highlighted based on the percentage of missing values**.""")
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Boxplot""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Creation of a basic boxplot using **`.mark_boxplot()` method**""")
    return


@app.cell
def _(alt, df):
    alt.Chart(df).mark_boxplot().encode(x="OverallQual:O", y="SalePrice:Q", color="OverallQual:N").properties(
        width=500, height=300
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Heatmaps""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Creation of a basic heatmap using **`.mark_rect()` method**.""")
    return


@app.cell
def _(alt, train):
    alt.Chart(train).mark_rect().encode(
        x="MSZoning", y="ExterQual", color="average(SalePrice)", tooltip=["MSZoning", "ExterQual", "average(SalePrice)"]
    ).properties(width=500, height=300)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Bindings, Selections & Conditions""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Here you can **select the `KitchenQual` feature** from a **dropdown menu** and see how the graph changes color!"""
    )
    return


@app.cell
def _(alt, train):
    input_dropdown = alt.binding_select(options=list(train["KitchenQual"].unique()), name="Lot Shape")
    _selection = alt.selection_point(fields=["KitchenQual"], bind=input_dropdown)
    color = alt.condition(_selection, alt.Color("KitchenQual:N", legend=None), alt.value("lightgray"))
    alt.Chart(train).mark_point().encode(
        x="GrLivArea", y="SalePrice", color=color, tooltip=["GrLivArea", "SalePrice"]
    ).properties(width=500, height=300).add_params(_selection).configure_axis(grid=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Interactive Chart with Cross-Highlight""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    In this more advanced example, I use the `ExterQual` feature as a filter for a **binned heatmap**.

    **Click** on the bar chart **bars to change the heatmap**!
    """
    )
    return


@app.cell
def _(alt, train):
    pts = alt.selection_point(encodings=["x"])

    rect = (
        alt.Chart(train)
        .mark_rect()
        .encode(
            x=alt.X("GrLivArea", bin=alt.Bin(maxbins=40)),
            y=alt.Y("GarageArea", bin=alt.Bin(maxbins=40)),
            color="average(SalePrice)",
        )
        .properties(width=500, height=300)
        .transform_filter(pts)
    )

    bar = (
        alt.Chart(train)
        .mark_bar()
        .encode(
            x="ExterQual:N",
            y="count()",
            color=alt.condition(pts, alt.ColorValue("steelblue"), alt.ColorValue("grey")),
            tooltip=["ExterQual", "count()"],
        )
        .properties(width=550, height=200)
        .add_params(pts)
    )


    alt.vconcat(rect, bar).resolve_legend(color="independent", size="independent").configure_axis(grid=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Dot Dash Plot

    A Dot Dash Plot is basically a **scatter plot** with **both axis removed** and replaced with **barcode plots** (aka strip plots), which allow you to **see the distribution of values** of each measure used in the scatter plot.
    """
    )
    return


@app.cell
def _(alt, train):
    # Configure the options common to all layers
    brush = alt.selection_interval()
    base = alt.Chart(train).add_params(brush)

    # Configure the points
    points = base.mark_point().encode(
        x=alt.X("GrLivArea", title=""),
        y=alt.Y("SalePrice", title=""),
        color=alt.condition(brush, "KitchenQual", alt.value("grey")),
    )

    # Configure the ticks
    tick_axis = alt.Axis(labels=False, domain=False, ticks=False)

    x_ticks = base.mark_tick().encode(
        alt.X("GrLivArea", axis=tick_axis),
        alt.Y("KitchenQual", title="", axis=tick_axis),
        color=alt.condition(brush, "KitchenQual", alt.value("lightgrey")),
    )

    y_ticks = base.mark_tick().encode(
        alt.X("KitchenQual", title="", axis=tick_axis),
        alt.Y("SalePrice", axis=tick_axis),
        color=alt.condition(brush, "KitchenQual", alt.value("lightgrey")),
    )

    # Build the chart
    (y_ticks | (points & x_ticks)).configure_axis(grid=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Multifeature Scatter Plot

    Let's create a scatter plot with **multiple feature encodings**.

    With `.interactive()` you can zoom in. You can also **click on legend** to select specific `KitchenQual` values.
    """
    )
    return


@app.cell
def _(alt, train):
    _selection = alt.selection_point(fields=["KitchenQual"], bind="legend")
    alt.Chart(train).mark_circle().encode(
        alt.X("GrLivArea", scale=alt.Scale(zero=False)),
        alt.Y("GarageArea", scale=alt.Scale(zero=False, padding=1)),
        color="KitchenQual",
        size=alt.Size("SalePrice", bin=alt.Bin(maxbins=10), title="SalePrice"),
        opacity=alt.condition(_selection, alt.value(1), alt.value(0.2)),
        tooltip=["GrLivArea", "SalePrice"],
    ).properties(width=500, height=500).add_params(_selection).configure_axis(grid=False).interactive()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Scatter Matrix

    Scatter matrix are one of the most common graph you'll see on Kaggle. It consists of several **pair-wise scatter plots** of variables presented in a **matrix format**, useful to visualize **multiple relationships** between a pair of variables.

    In Altair this can be achieved using a RepeatChart, let's see how!
    """
    )
    return


@app.cell
def _(alt, train):
    alt.Chart(train).mark_circle().encode(
        alt.X(alt.repeat("column"), type="quantitative"), alt.Y(alt.repeat("row"), type="quantitative"), color="KitchenQual"
    ).properties(width=300, height=300).repeat(
        # Here we tell Altair we want to repeat out scatter plots for each row-column pair
        row=["GrLivArea", "GarageArea", "TotalBsmtSF"],
        column=["TotalBsmtSF", "GarageArea", "GrLivArea"],
    ).configure_axis(grid=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Layered Histogram

    Using Altair, we can make overlapping histograms or layers histograms from data:
    """
    )
    return


@app.cell
def _(alt, train):
    alt.Chart(train).mark_bar(opacity=0.5, binSpacing=0).encode(
        alt.X("SalePrice:Q", bin=alt.Bin(maxbins=50)), alt.Y("count()", stack=None), alt.Color("MSZoning:N")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### To be continued""")
    return


if __name__ == "__main__":
    app.run()
