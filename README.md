# Volatility Surface Analyzer

<img width="597" height="402" alt="Volatility Surface Analyzer Screenshot" src="https://github.com/user-attachments/assets/30f2d06e-af54-41ee-a71a-b131be4587da" />

## Overview

This project analyzes implied volatility surfaces using live options chain data.

The app takes a ticker as input and produces:
- raw implied volatility surface
- smoothed implied volatility surface
- volatility smile
- volatility term structure
- data quality report

The goal of this project is to understand how implied volatility behaves across strikes and maturities, and to visualize where real options data can become sparse, noisy, or unstable.

This project is not investement advice. It is meant to be an analytical and educational tool for studying volatility surfaces.

## Background: Implied Volatility

Implied volatility is a forward-looking metric that represents the market's expectation of future uncertainty in an option's price. It is not directly observable, rather it is inferred from option prices using an option pricing model.

In this project, implied volatility is obtained by reversing the Black-Scholes pricing model. For a given market price, we solve for the volatility that corresponds to the theoretical model price.

Because this inversion depends on numerical methods and the vega of the option, it can be unstable in certain regions, particularly for short-dated, illiquid, or deep out-of-the-money options.

The project also uses the implied volatility provided by yfinance as a fallback when the internal implied volatility calculation fails.

## Methodology

The project takes the following approach:

1. A ticker is provided through the Streamlit frontend.
2. Options chain data is fetched using yfinance.
3. The raw options data is cleaned and standardized.
4. Mid prices are calculated from bid and ask quotes when available.
5. Implied volatility is calculated using Black-Scholes inversion.
6. If the calculation fails, the yfinance implied volatility value is used as a fallback.
7. The cleaned data is transformed into a surface grid.
8. Raw and smoothed volatility surfaces are visualized.
9. Volatility smiles and term structures are generated.
10. A data quality report is shown to highlight how much usable data was available.

## Features

- Live ticker-based options chain fetching
- Data cleaning and validation pipeline
- Black-Scholes option pricing
- Implied volatility calculation using bisection
- Fallback to provider implied volatility when calculation fails
- Raw implied volatility surface
- Smoothed implied volatility surface
- Volatility smile visualization
- Volatility term structure visualization
- Streamlit frontend
- FastAPI backend
- Data quality report

## Project Structure

```
Volatility-Surface-Analyzer/
│
├── api/                  # FastAPI backend
├── frontend/             # Streamlit frontend
├── data/                 # yfinance fetcher and options cleaner
├── computation/          # Black-Scholes, implied volatility, smoothing
├── visualization/        # Surface, smile, term structure plots
├── README.md
├── requirements.txt
└── LICENSE
```

## How to Run

Clone the repository and install the requirements:

```
pip install -r requirements.txt
```

Start the FastAPI backend:

```
uvicorn api.main:app --reload
```

In a separate terminal, start the Streamlit frontend:

```
streamlit run frontend/streamlit_app.py
```

Then enter a ticker such as:

```
AAPL
TSLA
MSFT
SPY
```

The app will fetch the options chain, process the data, and display the selected volatility plot.

## Data Quality

Real options data is often messy. Some tickers may have sparse options chains, missing quotes, stale prices, or very wide bid-ask spreads.

Because of this, the project includes a data quality report showing:
- number of raw rows fetched
- number of clean rows retained
- number of rejected rows
- usable expirations
- number of call and put contracts
- quality breakdown of retained rows
- whether the surface is considered ready for plotting

The cleaner is intentionally not too aggressive. It removes only clearly unusable rows and keeps lower-quality rows marked with quality flags.

## Limitations

- yfinance data may be sparse, stale, or incomplete.
- The project is not intended for trading decisions.
- Black-Scholes is a simplified model and does not capture all real market effects.
- Most listed options are American-style, while the model used here is based on European option pricing.
- Smoothing is used as a visual aid and should not be interpreted as the true market surface.
- Some tickers may not have enough reliable options data to generate a useful surface.

## Future Extensions

- Better handling of sparse volatility grids
- Support for premium options data APIs
- Arbitrage constraint checks
- More configurable frontend controls
- Docker support

## License

This project is licensed under the MIT License.

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.