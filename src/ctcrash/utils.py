from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap


def read_csv(
    csv_file: Path, columns: list[str] | None = None, **kwargs
) -> pd.DataFrame:
    df = pd.read_csv(csv_file, skiprows=[0], **kwargs)
    if columns:
        return df[columns]
    return df


def create_pivot_table(df, index, columns, values="CrashId", enable_totals=True):
    return df.pivot_table(
        index=index,
        columns=columns,
        values=values,
        aggfunc="count",
        observed=False,
        **{"margins": True, "margins_name": "Total"} if enable_totals else {},
    )


def pivot_table_with_totals_to_heatmap(pivot_table):
    # Create a mask for the totals
    mask = pd.DataFrame(False, index=pivot_table.index, columns=pivot_table.columns)
    mask.loc["Total", :] = True
    mask.loc[:, "Total"] = True

    # Create the heatmap
    plt.figure(figsize=(12, 8))

    # Heatmap for the main data excluding totals
    sns.heatmap(pivot_table, annot=True, fmt="g", cmap="flare", mask=mask, cbar=False)

    # Overlay heatmap for the totals with a different color
    sns.heatmap(pivot_table, annot=True, fmt="g", cmap="crest", mask=~mask, cbar=False)

    return plt


def create_map(df):
    # Create a base map
    base_map = folium.Map(
        location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=13
    )

    # Prepare data for heatmap
    heat_data = [[row["Latitude"], row["Longitude"]] for index, row in df.iterrows()]

    # Create and add heatmap to base map
    HeatMap(heat_data).add_to(base_map)
    return base_map


class CTCrashData:
    def __init__(self):
        self.df = pd.DataFrame()

    def load_csv(
        self, csv_file: Path, columns: list[str] | None = None, **kwargs
    ) -> None:
        new_df = read_csv(csv_file, columns, **kwargs)
        if self.df.empty:
            self.df = new_df
        else:
            self.df.merge(new_df, on="CrashId")

    def create_pivot_table(
        self, index: str, columns: str, values: str = "CrashId"
    ) -> pd.DataFrame:
        return create_pivot_table(self.df, index, columns, values)

    def create_heatmap_from_pivot_table_with_totals(self, pivot_table: pd.DataFrame):
        return pivot_table_with_totals_to_heatmap(pivot_table)
