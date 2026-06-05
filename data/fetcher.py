from datetime import date, datetime
from typing import Any, Iterable

import pandas as pd
import yfinance as yf

COLUMNS: list[str] = [
    "contractSymbol",
    "lastTradeDate",
    "strike",
    "lastPrice",
    "bid",
    "ask",
    "volume",
    "openInterest",
    "impliedVolatility",
    "inTheMoney",
]


def fetch_spot_price(ticker: str) -> float:
    ticker_object = yf.Ticker(ticker)

    fast_data = ticker_object.fast_info

    if fast_data.last_price:
        return fast_data.last_price

    if fast_data.previous_close:
        return fast_data.previous_close

    history: pd.DataFrame = ticker_object.history(period="5d")
    if not history.empty and "Close" in history:
        close: pd.Series[Any] = history["Close"].dropna()
        if not close.empty and close.iloc[-1] > 0:
            return float(close.iloc[-1])

    raise ValueError(f"Could not fetch spot price for ticker: {ticker}.")


def fetch_expirations(
    ticker: str,
    *,
    min_days: int = 7,
    max_days: int = 180,
    max_expirations: int | None = 8,
) -> list[str]:
    symbol = yf.Ticker(ticker)
    expirations: list = list(symbol.options)

    today = date.today()
    selected: list = []

    for expiry in expirations:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        diff: int = (expiry_date - today).days

        if min_days <= diff <= max_days:
            selected.append(expiry)

        if max_expirations is not None:
            selected = selected[:max_expirations]

    return selected


def fetch_option_chain(
    ticker: str,
    *,
    expirations: Iterable[str] | None = None,
    min_days: int = 7,
    max_days: int = 365,
    max_expirations: int | None = 12,
    include_calls: bool = True,
    include_puts: bool = True,
) -> pd.DataFrame:
    if not include_calls and not include_puts:
        raise ValueError("Either call or put required.")

    ticker = ticker.upper().strip()
    symbol = yf.Ticker(ticker)

    spot_price: float = fetch_spot_price(ticker)

    if expirations is None:
        selected_expirations: list[str] = fetch_expirations(
            ticker,
            min_days=min_days,
            max_days=max_days,
            max_expirations=max_expirations,
        )
    else:
        selected_expirations = list(expirations)

    output_columns: list[str] = [
        "underlying_ticker",
        "spot_price",
        "expiration_date",
        "contract_type",
        *COLUMNS,
    ]

    if not selected_expirations:
        return pd.DataFrame(columns=output_columns)

    frames: list = []

    for expiry in selected_expirations:
        chain = symbol.option_chain(expiry)

        if include_calls:
            calls = chain.calls.copy()
            calls["underlying_ticker"] = ticker
            calls["spot_price"] = spot_price
            calls["expiration_date"] = expiry
            calls["contract_type"] = "call"
            frames.append(calls)

        if include_puts:
            puts = chain.puts.copy()
            puts["underlying_ticker"] = ticker
            puts["spot_price"] = spot_price
            puts["expiration_date"] = expiry
            puts["contract_type"] = "put"
            frames.append(puts)

    if not frames:
        return pd.DataFrame(columns=output_columns)

    df = pd.concat(frames, ignore_index=True)

    return df[output_columns]
