import marimo

__generated_with = "0.19.7"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # KNMI Weather Data Export to Parquet

    ## Purpose
    This notebook fetches hourly weather data from the KNMI (Royal Netherlands Meteorological Institute) and exports it to Parquet format for use in the Smart HVAC Steering project.

    ## Data Source
    - **Provider:** KNMI (Koninklijk Nederlands Meteorologisch Instituut)
    - **Station:** Eindhoven (code 370)
    - **Temporal Resolution:** Hourly
    - **Date Range:** 2023-01-01 to 2025-12-31

    ## References
    - [knmi-py Documentation](https://knmy.readthedocs.io/en/latest/)
    - [knmi-py PyPI](https://pypi.org/project/knmi-py/#description)
    - [Weather Provider API](https://pypi.org/project/weather_provider_api/)
    - [Alliander Weather Provider API (GitHub)](https://github.com/alliander-opensource/Weather-Provider-API)

    ---

    ## Table of Contents
    1. [Setup & Imports](#1-setup--imports)
    2. [Data Fetching Function](#2-data-fetching-function)
    3. [Fetch Weather Data](#3-fetch-weather-data)
    4. [Export to Parquet](#4-export-to-parquet)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Important: Timestamp Conventions

    ### KNMI Timezone & DST
    - **KNMI uses UTC year-round** (no daylight saving time adjustments)
    - Local Netherlands time is UTC+1 in winter and UTC+2 in summer
    - The exported KNMI parquet contains exactly 24 timestamps per day, confirming UTC timeline

    ### Hour-Label Convention
    KNMI documents that the timestamp indicates the **end of the measuring interval** preceding that timestamp:
    - Example: Hour 17:00 UTC represents the measurement from 16:00–17:00 UTC

    ### Alignment with BMS Data
    When comparing with Building Management System (BMS) data:
    - **BMS** typically logs snapshots at the **start of each hour** (start-of-interval)
    - **KNMI** timestamps represent **end-of-interval**
    - The `knmi-py` library subtracts 1 hour when building the datetime index (HH → HH-1)

    **Result:** A constant **+1 hour shift** is needed for KNMI data to align with BMS snapshots.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Technical Details

    | Aspect | Description |
    |--------|-------------|
    | KNMI Timeline | Fixed UTC, no DST transitions (always 24 hours/day) |
    | KNMI Convention | End-of-interval (17:00 = data from 16:00-17:00) |
    | BMS Convention | Start-of-interval (10:00 = snapshot at 10:00) |
    | knmi-py Adjustment | Subtracts 1 hour from KNMI hour codes |
    | Required Shift | KNMI +1h OR BMS -1h for alignment |

    > **Reference:** [KNMI Data Documentation](https://english.knmidata.nl)

    ---

    ## 1. Setup & Imports
    """)
    return


@app.cell
def _():
    import os
    from datetime import datetime

    import knmi
    import pandas as pd
    return datetime, knmi, os, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Data Fetching Function

    ### KNMI Variable Codes
    | Code | Description | Raw Unit | Converted Unit |
    |------|-------------|----------|----------------|
    | T | Temperature | 0.1 °C | °C |
    | FH | Wind Speed (hourly mean) | 0.1 m/s | m/s |
    | U | Relative Humidity | % | % |
    | Q | Global Radiation | J/cm² | W/m² |
    | N | Cloud Cover | oktas (0-9) | oktas |
    | RH | Precipitation | 0.1 mm | mm |

    > **Note:** KNMI stores temperature, wind, and precipitation in 0.1 units, requiring division by 10 for standard units.
    """)
    return


@app.cell
def _(knmi, pd):
    def get_knmi_hourly_weather(start_date: str, end_date: str, station_code: int = 370) -> pd.DataFrame:
        """
        Fetch hourly weather data from KNMI and convert to standard units.

        Parameters
        ----------
        start_date : str
            Start date in 'YYYY-MM-DD' format
        end_date : str
            End date in 'YYYY-MM-DD' format
        station_code : int, optional
            KNMI station code (default: 370 = Eindhoven)

        Returns
        -------
        pd.DataFrame
            Hourly weather data with columns: timestamp, temp_outdoor, wind_speed,
            rel_humidity, cloud_cover, precip_amount, solar_rad_W_m2
        """
        print(f"Fetching KNMI hourly data for Station {station_code}")
        print(f"Date range: {start_date} to {end_date}")

        # Fetch raw data from KNMI API
        df = knmi.get_hour_data_dataframe(stations=[station_code], start=start_date, end=end_date)

        # Column mapping: KNMI codes -> readable names
        rename_map = {
            "T": "temp_outdoor",  # Temperature (0.1 °C)
            "FH": "wind_speed",  # Hourly mean wind speed (0.1 m/s)
            "U": "rel_humidity",  # Relative Humidity (%)
            "Q": "solar_rad_raw",  # Global Radiation (J/cm²)
            "N": "cloud_cover",  # Cloud Cover (oktas: 0=Clear, 8=Overcast, 9=Obscured)
            "RH": "precip_amount",  # Hourly precipitation (0.1 mm)
        }

        # Filter to only existing columns and rename
        existing_cols = [c for c in rename_map.keys() if c in df.columns]
        df = df[existing_cols].rename(columns=rename_map)

        # Unit conversions
        if "temp_outdoor" in df.columns:
            df["temp_outdoor"] = df["temp_outdoor"] / 10.0  # 0.1°C -> °C

        if "wind_speed" in df.columns:
            df["wind_speed"] = df["wind_speed"] / 10.0  # 0.1 m/s -> m/s

        if "precip_amount" in df.columns:
            df.loc[df["precip_amount"] == -1, "precip_amount"] = 0  # -1 = trace amount (<0.05mm)
            df["precip_amount"] = df["precip_amount"] / 10.0  # 0.1 mm -> mm

        if "solar_rad_raw" in df.columns:
            # J/cm² (hourly sum) -> W/m² (average power)
            # Conversion: val * 10,000 (cm² to m²) / 3600 (J to W) ≈ 2.778
            df["solar_rad_W_m2"] = df["solar_rad_raw"] * 2.77778
            df = df.drop(columns=["solar_rad_raw"])

        # Reset index to make timestamp a column
        df = df.reset_index(names="timestamp")

        print(f"Retrieved {len(df):,} rows")
        print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}\n")

        return df
    return (get_knmi_hourly_weather,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Fetch Weather Data
    """)
    return


@app.cell
def _(get_knmi_hourly_weather):
    # Fetch KNMI data for Eindhoven (station 370)
    df_KNMI_weather = get_knmi_hourly_weather("2023-01-01", "2025-12-31", station_code=370)

    # Preview data
    df_KNMI_weather.head(10)
    return (df_KNMI_weather,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Data Quality Check
    """)
    return


@app.cell
def _(df_KNMI_weather):
    # Statistical summary
    df_KNMI_weather.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Export to Parquet
    """)
    return


@app.cell
def _(datetime, os, pd):
    def save_dataframe_to_parquet(df: pd.DataFrame, output_path: str, file_identifier: str) -> str | None:
        """
        Save DataFrame to Parquet with date-prefixed filename.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to save
        output_path : str
            Directory path for output file
        file_identifier : str
            Identifier to include in filename

        Returns
        -------
        str | None
            Full path to saved file, or None if save failed
        """
        try:
            os.makedirs(output_path, exist_ok=True)

            current_date = datetime.now().strftime("%Y-%m-%d")
            filename = f"{current_date}_{file_identifier}.parquet"
            full_path = os.path.join(output_path, filename)

            df.to_parquet(full_path, index=False)
            print(f"Saved to: {full_path}")

            return full_path

        except Exception as e:
            print(f"Error saving {file_identifier}: {e}")
            return None
    return (save_dataframe_to_parquet,)


@app.cell
def _(df_KNMI_weather, os, save_dataframe_to_parquet):
    # Configure output path
    raw_path = os.getenv("DATA_RAW_PATH", "data/knmi/")

    # Save KNMI weather data
    save_dataframe_to_parquet(df_KNMI_weather, raw_path, "01_KNMI_weather")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Output Summary

    The exported Parquet file contains:
    - **26,304 hourly rows** (2023-01-01 00:00 → 2025-12-31 23:00)
    - Perfect hourly cadence with no gaps
    - No missing temperature values

    ### Output Columns
    | Column | Unit | Description |
    |--------|------|-------------|
    | timestamp | datetime | UTC timestamp (start-of-interval after knmi-py adjustment) |
    | temp_outdoor | °C | Outdoor temperature |
    | wind_speed | m/s | Hourly mean wind speed |
    | rel_humidity | % | Relative humidity |
    | cloud_cover | oktas | Cloud cover (0-9) |
    | precip_amount | mm | Hourly precipitation |
    | solar_rad_W_m2 | W/m² | Global solar radiation |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Note on Resampling

    When resampling this data for alignment with other sources:

    ```python
    df.resample("1h", label="left", closed="left").mean()
    ```

    This ensures consistent left-aligned intervals matching BMS snapshot convention.
    """)
    return


if __name__ == "__main__":
    app.run()
