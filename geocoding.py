import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import re
    import urllib

    import altair as alt
    import polars as pl
    import requests


    def locatieserver(query):
        """Get lat long coordinates for Dutch address"""

        PDOK = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/free"

        def extract_long_lat(point) -> list[str]:
            "Extract coordinates from POINT(x.x y,y) text"
            return re.findall(r"\d+\.\d+", point)

        query_params = {
            "fl": "id nummeraanduiding_id centroide_ll huisnummer postcode",
            "fq": "type:adres",
            "df": "tekst",
            "start": 0,
            "rows": 1,
            "sort": "score desc,sortering asc,weergavenaam asc",
            "wt": "json",
        }
        params = urllib.parse.urlencode({**{"q": query}, **query_params}, quote_via=urllib.parse.quote)

        # Note pdok returns (long, lat)
        long, lat = extract_long_lat(
            requests.get(PDOK, params, timeout=100).json().get("response").get("docs")[0].get("centroide_ll")
        )
        return {"lat": float(lat), "long": float(long)}
    return alt, locatieserver, pl


@app.cell
def _(locatieserver, pl):
    df = (
        pl.read_excel("plugin.xlsx", sheet_id=2)
        .with_columns(
            pl.concat_str([pl.col("Straat"), pl.col("Nummer"), pl.col("Postcode"), pl.col("Plaats")], separator=" ")
            .alias("Adres")
            .map_elements(locatieserver, return_dtype=pl.Struct({"lat": pl.Float64, "lon": pl.Float64}))
        )
        .unnest(pl.col("Adres"))
    )
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _():
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(df.filter(pl.col("is_hoofdlocatie") == 1)).mark_circle().encode(
        longitude="long:Q", latitude="lat:Q", color="is_gecontracteerd:N", tooltip=["Naam", "Plaats"]
    ).project("mercator").properties(width=500, height=400)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
