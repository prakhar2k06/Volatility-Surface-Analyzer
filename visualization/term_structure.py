import numpy as np
import pandas as pd
import plotly.graph_objects as go


def plot_term_structure(
    df: pd.DataFrame,
    spot: float,
    strikes_to_plot=None,
    title: str = "Volatility Term Structure",
) -> go.Figure:

    strikes = df.index.values
    maturities = df.columns.values

    if len(strikes) == 0:
        raise ValueError("Cannot plot term structure from an empty dataframe.")

    if strikes_to_plot is None:
        atm_idx = np.argmin(np.abs(strikes - spot))
        strikes_to_plot = [strikes[atm_idx]]

    fig = go.Figure()

    for K in strikes_to_plot:
        if K not in df.index:
            nearest_idx = np.argmin(np.abs(strikes - K))
            K = strikes[nearest_idx]

        fig.add_trace(
            go.Scatter(
                x=maturities.tolist(),
                y=df.loc[K].values.tolist(),
                mode="lines+markers",
                name=f"K = {K:.1f}",
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="Maturity",
        yaxis_title="Implied Volatility",
        width=800,
        height=500,
    )

    return fig
