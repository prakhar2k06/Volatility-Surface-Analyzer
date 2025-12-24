import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_smile(df: pd.DataFrame) -> None:
    strikes = df.index.values
    maturities = df.columns.values
    n = len(maturities)
    idxs = [0, n // 2, n-1]

    plt.figure(figsize = (10, 7))

    for i in idxs:
        maturity = maturities[i]
        iv = df[maturity].values
        plt.plot(strikes, iv, marker="o", label = f"T = {maturity:.2f}y")

    plt.xlabel("Strike")
    plt.ylabel("Implied Volatility")
    plt.title(f"Volatility Smile")
    plt.legend()
    plt.grid(True)

    plt.show()
