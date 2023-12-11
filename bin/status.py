import argparse
import sys
import numpy as np
import pandas as pd
import plotly.express as px
from prettytable import MARKDOWN, PrettyTable


def main():
    options = parse_args()

    info = pd.read_csv(options.info)
    status = pd.read_csv(options.status)

    status = status.sort_values("date", ascending=False)
    combined = status.set_index("story")\
                     .join(info.set_index("story"))\
                     .sort_values(["category", "title"])\
                     .reset_index()\
                     [["title", "date", "words", "target"]]
    no_target = combined[pd.isna(combined["target"])].assign(percent=0).fillna(0)
    with_target = combined[pd.notna(combined["target"])]
    with_target = with_target.assign(percent=(100 * with_target["words"] / with_target["target"]).astype(int))

    for_table = pd.concat([with_target, no_target]).sort_values(["percent"], ascending=False)
    for_table = for_table.drop_duplicates(["title"])
    print(for_table.to_markdown(index=False))

    with_target["percentage"] = with_target["words"] / with_target["target"]
    fig = px.line(with_target, x="date", y="percentage", color="title", facet_row="target", line_shape="vh")
    fig.update_yaxes(range=[0.0, 1.1], tick0=0.0, dtick=0.2)
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
