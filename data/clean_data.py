from raw_data import fetch_option_chain
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import timedelta

MAX_SPREAD = 0.3
MIN_DTE = 7
STRIKE_LOWER = 0.8
STRIKE_UPPER = 1.2

def clean_option_chain(df: pd.DataFrame, spot_price: float) -> pd.DataFrame:
    df["expiryDate"] = pd.to_datetime(df["expiryDate"])
    df = df[(df["bid"] > 0) & (df["ask"] > 0)].copy()
    df["midPrice"] = (df["bid"] + df["ask"]) / 2
    df = df[df["midPrice"] > 0].copy()
    df = df[(df["ask"] - df["bid"]) / df["midPrice"] < MAX_SPREAD].copy()
    df = df[(df["volume"] > 0) | (df["openInterest"] > 0)].copy()
    today = pd.Timestamp.today().normalize()
    df = df[df["expiryDate"] - today > timedelta(days = MIN_DTE)].copy()
    df = df[(df["strike"] >= STRIKE_LOWER * spot_price) & (df["strike"] <= STRIKE_UPPER * spot_price)].copy()

    return df
