import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_volatility_surface(df: pd.DataFrame) -> None:
    x = df.index.values
    y = df.columns.values
    X, Y = np.meshgrid(x, y)
    Z = df.values.T
    fig = plt.figure(figsize = (10, 7))
    ax = fig.add_subplot(111, projection = "3d")
    surface = ax.plot_surface(X, Y, Z, cmap = "viridis", edgecolor = "none", alpha = 0.9)
    fig.colorbar(surface, shrink = 0.6, aspect = 5)
    ax.set_xlabel("Strike")
    ax.set_ylabel("Maturity (years)")
    ax.set_zlabel("Implied Volatility")
    ax.set_title("Implied Volatility Surface")
    plt.show() 


