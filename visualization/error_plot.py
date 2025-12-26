import plotly.graph_objects as go
import numpy as np
import pandas as pd

def plot_error_surface(df: pd.DataFrame, title: str = "Error Surface") -> None:
    '''
    Plots error between true volatility surface and calculated volatility surface.
    '''
    strikes = df.index.values
    maturities = df.columns.values

    X, Y = np.meshgrid(maturities, strikes)
    Z = df.values

    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale="Viridis", showscale=True)])

    fig.update_layout(title=title, scene = dict(xaxis_title="Maturity", yaxis_title="Strike", zaxis_title="Error",),width=800,height=600,)

    fig.show()
