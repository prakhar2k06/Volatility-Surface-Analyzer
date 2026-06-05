import numpy as np
import pandas as pd

from computation.black_scholes import calculate_theoretical_value


def _get_market_price(row: pd.Series) -> float:
    mid = row.get("mid", np.nan)
    last_price = row.get("lastPrice", np.nan)

    if mid > 0 and pd.notna(mid):
        return float(mid)

    if last_price > 0 and pd.notna(last_price):
        return float(last_price)

    return np.nan


def calculate_implied_volatility(row) -> float:
    market_price: float = _get_market_price(row)
    spot_price: float = row["spot_price"]
    strike: float = row["strike"]
    time_to_expiry: float = row["time_to_expiry"]
    contract_type: str = row["contract_type"]
    risk_free_rate: float = 0.04

    max_iter: int = 100
    tol: float = 1e-6

    if (
        pd.isna(market_price)
        or pd.isna(spot_price)
        or pd.isna(strike)
        or pd.isna(time_to_expiry)
        or market_price <= 0
        or spot_price <= 0
        or strike <= 0
        or time_to_expiry <= 0
    ):
        return np.nan

    low = 1e-8
    high = 4.0

    for i in range(max_iter):
        vol: float = (low + high) / 2
        mid_price: float = calculate_theoretical_value(
            spot_price, strike, time_to_expiry, vol, risk_free_rate, contract_type
        )

        error: float = mid_price - market_price

        if abs(error) < tol:
            return vol

        if error < 0:
            low: float = vol

        else:
            high: float = vol

    return np.nan


def calculate_implied_volatility_df(df) -> pd.DataFrame:
    new_df: pd.DataFrame = df.copy()
    new_df["computed_iv"] = new_df.apply(calculate_implied_volatility, axis=1)

    computed_valid = (
        new_df["computed_iv"].notna()
        & (new_df["computed_iv"] > 0)
        & (new_df["computed_iv"] <= 5.0)
    )

    provider_valid = (
        new_df["provider_iv"].notna()
        & (new_df["provider_iv"] > 0)
        & (new_df["provider_iv"] <= 5.0)
    )

    new_df["final_iv"] = np.where(
        computed_valid,
        new_df["computed_iv"],
        np.where(provider_valid, new_df["provider_iv"], np.nan),
    )

    new_df["iv_source"] = np.where(
        computed_valid,
        "computed",
        np.where(provider_valid, "provider_fallback", "unavailable"),
    )

    return new_df
