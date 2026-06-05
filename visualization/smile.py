import pandas as pd
import plotly.graph_objects as go


def plot_smile(
    df: pd.DataFrame,
    maturities_to_plot=None,
    title: str = "Volatility Smile",
) -> go.Figure:

    strikes = df.index.values
    maturities = df.columns.values

    if maturities_to_plot is None:
        maturities_to_plot = maturities

    fig = go.Figure()

    for T in maturities_to_plot:
        if T not in df.columns:
            continue

        fig.add_trace(
            go.Scatter(
                x=strikes.tolist(),
                y=df[T].values.tolist(),
                mode="lines+markers",
                name=f"T = {T:.2f}y",
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="Strike",
        yaxis_title="Implied Volatility",
        width=800,
        height=500,
    )

    return fig
