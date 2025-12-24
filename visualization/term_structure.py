import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_term_structure(df: pd.DataFrame, spot: float) -> None:
    strikes = df.index.values
    maturities = df.columns.values
    atm_idx = np.argmin(np.abs(strikes - spot))
    idxs = [atm_idx - 1, atm_idx, atm_idx + 1]

    plt.figure(figsize = (10, 7))

    for i in idxs:
        strike = strikes[i]
        iv = df.loc[strike].values
        plt.plot(maturities, iv, marker = "o", label = f"K = {strike}")

    plt.xlabel("Maturity (years)")
    plt.ylabel("ATM Implied Volatility")
    plt.title(f"Near-ATM Term Structure")
    plt.legend()
    plt.grid(True)

    plt.show()

