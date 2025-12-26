import numpy as np
import pandas as pd
import plotly.graph_objects as go

def plot_term_structure(df: pd.DataFrame, spot: float) -> None:
    '''
    Plots interactive term structure for various strikes.
    '''
    strikes = df.index.values
    maturities = df.columns.values

    atm_idx = np.argmin(np.abs(strikes - spot))

    idxs = [0, atm_idx, -1]

    fig = go.Figure()

    for i in idxs:
        K = strikes[i]
        fig.add_trace(go.Scatter(x=maturities, y=df.loc[K].values, mode="lines+markers", name=f"K = {K:.1f}"))

    fig.update_layout(title="ATM Term Structure", xaxis_title="Maturity (T)", yaxis_title="Implied Volatility", width=800, height=500,)

    fig.show()
