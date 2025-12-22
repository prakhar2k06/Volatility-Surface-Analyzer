import yfinance as yf
import pandas as pd

def fetch_option_chain(ticker_object: yf.Ticker):
    df = pd.DataFrame()
    for expiry_date in ticker_object.options:
        chain = ticker_object.option_chain(expiry_date)

        calls = chain.calls
        calls["expiryDate"] = expiry_date
        calls["optionType"] = "call"

        puts = chain.puts
        puts["expiryDate"] = expiry_date
        puts["optionType"] = "put"

        df = pd.concat([df, calls, puts], ignore_index=True)

    return df
