import pandas as pd
import plotly.graph_objects as go

def plot_smile(df: pd.DataFrame, maturities_to_plot=None) -> None:
    '''
    Plots smile of the option for multiple maturities.
    '''
    strikes = df.index.values
    maturities = df.columns.values

    if maturities_to_plot is None:
        n = len(maturities)
        maturities_to_plot = maturities[2:-1]

    fig = go.Figure()

    for T in maturities_to_plot:
        fig.add_trace(go.Scatter(x=strikes, y=df[T].values, mode="lines+markers", name=f"T = {T:.2f}y"))

    fig.update_layout(title="Volatility Smile (Multiple Maturities)", xaxis_title="Strike (K)", yaxis_title="Implied Volatility", width=800, height=500,)

    fig.show()
