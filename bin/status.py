import argparse
from datetime import timedelta
import numpy as np
import pandas as pd
import plotly.express as px
from prettytable import MARKDOWN, PrettyTable
import sys


def main():
    options = parse_args()

    info = pd.read_csv(options.info)
    status = pd.read_csv(options.status).groupby("story").filter(lambda x: len(x) > 1)
    status = status.sort_values("date", ascending=False)

    df = status.set_index("story")\
               .join(info.set_index("story"))\
               .sort_values(["category", "title"])\
               .reset_index()\
               [["title", "date", "words"]]
    df["date"] = pd.to_datetime(df["date"]).dt.date
    print(df.drop_duplicates(["title"]).to_markdown(index=False))

    fig = px.line(df, x="date", y="words", color="title", line_shape="vh", markers=True)
    date_offset = timedelta(days=1)
    fig.update_xaxes(range=[min(df["date"]) - date_offset, max(df["date"]) + date_offset])
    fig.write_image(options.chart, width=1200)


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--chart", required=True, help="Chart filename")
    parser.add_argument("--info", required=True, help="Information about stories")
    parser.add_argument("--status", required=True, help="Status information")
    return parser.parse_args()


if __name__ == "__main__":
    main()
