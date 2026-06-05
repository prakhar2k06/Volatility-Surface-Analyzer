from datetime import date
from typing import Any

import numpy as np
import pandas as pd

REQUIRED_COLUMNS: list[str] = [
    "underlying_ticker",
    "spot_price",
    "expiration_date",
    "contract_type",
    "contractSymbol",
    "strike",
    "lastPrice",
    "bid",
    "ask",
    "volume",
    "openInterest",
    "impliedVolatility",
]


CLEAN_COLUMNS: list[str] = [
    "underlying_ticker",
    "spot_price",
    "expiration_date",
    "days_to_expiry",
    "time_to_expiry",
    "contract_type",
    "contractSymbol",
    "strike",
    "moneyness",
    "log_moneyness",
    "lastPrice",
    "bid",
    "ask",
    "mid",
    "spread",
    "spread_pct",
    "volume",
    "openInterest",
    "provider_iv",
    "computed_iv",
    "final_iv",
    "iv_source",
    "quality_flag",
]


def clean_option_chain(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    if raw_df.empty:
        return pd.DataFrame(columns=CLEAN_COLUMNS), _empty_report()

    _validate_required_columns(raw_df)

    df: pd.DataFrame = raw_df.copy()

    raw_rows: int = len(df)

    df = _standardize_types(df)
    df = _add_derived_columns(df)
    df = _add_price_columns(df)
    df = _add_iv_columns(df)
    df = _add_quality_flags(df)
    df = _drop_unusable_rows(df)

    clean_df = df[CLEAN_COLUMNS].reset_index(drop=True)

    quality_report: dict[str, Any] = _build_quality_report(raw_rows, clean_df)

    return clean_df, quality_report


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing: list[str] = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def _standardize_types(df: pd.DataFrame) -> pd.DataFrame:
    df["expiration_date"] = pd.to_datetime(df["expiration_date"]).dt.date

    numeric_columns: list[str] = [
        "spot_price",
        "strike",
        "lastPrice",
        "bid",
        "ask",
        "volume",
        "openInterest",
        "impliedVolatility",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["volume"] = df["volume"].fillna(0)
    df["openInterest"] = df["openInterest"].fillna(0)

    return df


def _add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    today = date.today()

    df["days_to_expiry"] = df["expiration_date"].apply(
        lambda expiry: (expiry - today).days
    )
    df["time_to_expiry"] = df["days_to_expiry"] / 365.0
    df["moneyness"] = df["strike"] / df["spot_price"]

    df["log_moneyness"] = np.where(
        df["moneyness"] > 0,
        np.log(df["moneyness"]),
        np.nan,
    )

    return df


def _add_price_columns(df: pd.DataFrame) -> pd.DataFrame:
    valid_market: pd.Series[bool] = (
        (df["bid"] > 0) & (df["ask"] > 0) & (df["ask"] >= df["bid"])
    )

    df["mid"] = np.where(
        valid_market,
        (df["bid"] + df["ask"]) / 2,
        np.nan,
    )

    df["spread"] = np.where(
        valid_market,
        df["ask"] - df["bid"],
        np.nan,
    )

    df["spread_pct"] = np.where(
        valid_market & (df["mid"] > 0),
        df["spread"] / df["mid"],
        np.nan,
    )

    return df


def _add_iv_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["provider_iv"] = df["impliedVolatility"]
    df["computed_iv"] = np.nan
    df["final_iv"] = df["provider_iv"]
    df["iv_source"] = "provider"

    return df


def _add_quality_flags(df: pd.DataFrame) -> pd.DataFrame:
    has_valid_mid: pd.Series[bool] = df["mid"].notna() & (df["mid"] > 0)
    has_liquidity: pd.Series[bool] = (df["volume"] > 0) | (df["openInterest"] > 0)
    has_spread: pd.Series[bool] = (df["spread_pct"] <= 0.5) & df["spread_pct"].notna()

    high_quality: pd.Series[bool] = has_valid_mid & has_liquidity & has_spread
    mid_quality: pd.Series[bool] = has_valid_mid & (has_liquidity | has_spread)

    df["quality_flag"] = np.select(
        [high_quality, mid_quality], ["high", "medium"], default="low"
    )

    return df


def _drop_unusable_rows(df: pd.DataFrame) -> pd.DataFrame:
    usable: pd.Series[bool] = (
        df["spot_price"].notna()
        & (df["spot_price"] > 0)
        & df["strike"].notna()
        & (df["strike"] > 0)
        & (df["days_to_expiry"] > 0)
        & df["provider_iv"].notna()
        & (df["provider_iv"] > 0)
        & (df["provider_iv"] <= 5)
        & df["moneyness"].notna()
        & df["log_moneyness"].notna()
    )

    return df[usable].copy()


def _build_quality_report(raw_rows: int, df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {
            "raw_rows": raw_rows,
            "clean_rows": 0,
            "rejected_rows": raw_rows,
            "usable_expirations": 0,
            "calls": 0,
            "puts": 0,
            "high_quality_rows": 0,
            "medium_quality_rows": 0,
            "low_quality_rows": 0,
            "surface_ready": False,
        }

    usable_expirations: int = df["expiration_date"].nunique()

    return {
        "raw_rows": raw_rows,
        "clean_rows": len(df),
        "rejected_rows": raw_rows - len(df),
        "usable_expirations": usable_expirations,
        "calls": int((df["contract_type"] == "call").sum()),
        "puts": int((df["contract_type"] == "put").sum()),
        "high_quality_rows": int((df["quality_flag"] == "high").sum()),
        "medium_quality_rows": int((df["quality_flag"] == "medium").sum()),
        "low_quality_rows": int((df["quality_flag"] == "low").sum()),
        "surface_ready": _is_surface_ready(df),
    }


def _is_surface_ready(df: pd.DataFrame) -> bool:
    if df.empty:
        return False

    if df["expiration_date"].nunique() < 3:
        return False

    points_per_expiry: pd.Series[int] = df.groupby("expiration_date")[
        "strike"
    ].nunique()

    if (points_per_expiry >= 5).sum() < 3:
        return False

    if len(df) < 30:
        return False

    return True


def _empty_report() -> dict:
    return {
        "raw_rows": 0,
        "clean_rows": 0,
        "rejected_rows": 0,
        "usable_expirations": 0,
        "calls": 0,
        "puts": 0,
        "high_quality_rows": 0,
        "medium_quality_rows": 0,
        "low_quality_rows": 0,
        "surface_ready": False,
    }
