import numpy as np
import pandas as pd
import plotly.graph_objects as go


def plot_volatility_surface(
    df: pd.DataFrame, title: str = "Volatility Surface"
) -> go.Figure:

    strikes = df.index.values
    maturities = df.columns.values

    X, Y = np.meshgrid(maturities, strikes)
    Z = df.values

    fig = go.Figure(
        data=[
            go.Surface(
                x=X.tolist(),
                y=Y.tolist(),
                z=Z.tolist(),
                colorscale="Viridis",
                showscale=True,
            )
        ]
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="Maturity",
            yaxis_title="Strike",
            zaxis_title="Implied Volatility",
        ),
        width=800,
        height=600,
    )

    return fig
