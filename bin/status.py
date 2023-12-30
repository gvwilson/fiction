import argparse
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from prettytable import MARKDOWN, PrettyTable
import sys

def main():
    options = parse_args()

    # Load data.
    info = pd.read_csv(options.info)
    status = pd.read_csv(options.status).groupby("story").filter(lambda x: len(x) > 1)
    status = status.sort_values("date")

    # Find word counts of active stories and show current totals.
    df = status.set_index("story")\
               .join(info.set_index("story"))\
               .sort_values(["title", "date"])\
               .reset_index()\
               [["title", "date", "words"]]
    df["date"] = pd.to_datetime(df["date"]).dt.date
    print(df.drop_duplicates(["title"], keep="last").to_markdown(index=False))

    # Find change over time.
    df["change"] = df.groupby("title").diff()["words"]
    change = df.dropna()[["date", "change"]].groupby(["date"]).sum("change").reset_index()
    change = change[change["change"] != 0]
    change = change.rename(columns={"change": "words"})
    change["title"] = "change"

    # Fill in missing dates.
    known = set(change["date"])
    min_date = min(change["date"])
    max_date = max(change["date"])
    full = {min_date + timedelta(days=d) for d in range(0, (max_date - min_date).days)}
    missing = pd.DataFrame({"title": "change", "words": 0, "date": list(sorted(full - known))})
    change = pd.concat([change, missing]).sort_values("date").reset_index()
    print(change[["date", "words"]].tail(n=7).to_markdown(index=False))

    # Combine stories and changes for plotting.
    df["kind"] = "story"
    change["kind"] = "delta"
    df = pd.concat([df[["title", "date", "words", "kind"]], change])

    # Plot.
    fig = px.line(df, x="date", y="words", color="title", line_shape="hv", facet_row="kind")
    date_offset = timedelta(days=1)
    fig.update_xaxes(range=[min_date - date_offset, max_date + date_offset])
    fig.update_yaxes(matches=None)
    if options.show:
        fig.show()
    fig.write_image(options.chart, width=1200)


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--chart", required=True, help="Chart filename")
    parser.add_argument("--info", required=True, help="Information about stories")
    parser.add_argument("--show", action="store_true", help="Show plot")
    parser.add_argument("--status", required=True, help="Status information")
    return parser.parse_args()


if __name__ == "__main__":
    main()
