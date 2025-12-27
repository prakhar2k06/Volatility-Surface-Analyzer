# Volatility Surface Analyzer

<img width="597" height="402" alt="Screenshot 2025-12-26 at 3 31 57 PM" src="https://github.com/user-attachments/assets/30f2d06e-af54-41ee-a71a-b131be4587da" />

## Overview
This project studies the behaviour of implied volatility and its surface in different market conditions using synthetic option prices.

We produce 
The project highlights:
- how implied volatility is calculated
- how volatility smiles and skews emerge
- how implied volatility structure varies in different markets
- where implied volatility can break down

## Background: Implied Volatility

Implied volatility is a crucial forward-looking metric that represents the market's expectation of future uncertainity in an option's price. It is not directly observable, rather it is inferred from option prices using an option pricing model.

In this project, implied volatility is obtained by reversing the black-scholes pricing model. For a given market price, we solve for the volatility that corresponds to the theoretical model price.

Because this inversion depends on numerical methods and the vega (option price sensitivity to volatility) of the option, it can be unstable in certain regions, particularly for short-dated or deep out-of-the-money options. 


## Methodology

The project takes the following approach:
1. A parametric volatility function generates true volatility surface.
2. European call options are priced using the black scholes formula.
3. Noise can be added optionally.
4. Implied volatility is back calculated using the bisection root finding method.
5. Volatility surfaces, smiles, and term structures are visualized.
6. Smoothing is done to balance noisy regions.
7. Error surfaces compare recovered implied volatility and true implied volatility.

**This project is easily extensible to real market data APIs such as yfinance.**

## Project Structure

```
Volatility-Surface-Analyzer/
│
├── data_generation/      # Synthetic volatility & price generation
├── computation/          # Black–Scholes, implied vol, smoothing, error
├── visualization/        # Surface, smile, term structure plots
├── experiments/          # Jupyter notebooks
├── README.md
└── LICENSE
```

## How to explore

Clone the repository and run the notebook in ```experiments/``` to:
- Generate volatility surfaces
- Generate smile and term structure graph
- Visualize differences between market regimes
- View smoothing in action

## Future Extensions:

- Arbitrage constraints
- Interactive UI for different parameters
- Extension to real market data
  
## License

This project is licensed under the MIT License.

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
  
