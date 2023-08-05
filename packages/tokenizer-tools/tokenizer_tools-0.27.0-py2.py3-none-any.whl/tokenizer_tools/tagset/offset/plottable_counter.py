from collections import Counter
import pandas as pd
import plotly.express as px


class PlottableCounter(Counter):
    def get_figure(self):
        df = (
            pd.DataFrame.from_dict(self, orient="index")
            .reset_index()
            .rename(columns={"index": "item", 0: "count"})
        )
        fig = px.bar(df, x="item", y="count")
        return fig
