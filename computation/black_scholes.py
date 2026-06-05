import numpy as np
from scipy.stats import norm


def calculate_theoretical_value(
    spot_price: float,
    strike: float,
    time_to_expiry: float,
    volatility: float,
    risk_free_rate: float,
    contract_type: str = "call",
) -> float:
    """
    Calculates the value of an option obtained via Black-Scholes Formula. Used to generate market prices and calculate implied volatility.
    """
    contract_type = contract_type.lower()

    if contract_type not in {"call", "put"}:
        raise ValueError("contract_type must be either 'call' or 'put'.")

    discounted_strike = strike * np.exp(-risk_free_rate * time_to_expiry)

    if time_to_expiry <= 1e-8 or volatility <= 1e-8:
        if contract_type == "call":
            return max(spot_price - discounted_strike, 0)
        return max(discounted_strike - spot_price, 0)

    sqrt_t = time_to_expiry**0.5

    d1 = (
        np.log(spot_price / strike)
        + (risk_free_rate + (volatility**2) / 2) * time_to_expiry
    ) / (volatility * sqrt_t)

    d2 = d1 - volatility * sqrt_t

    if contract_type == "call":
        return (spot_price * norm.cdf(d1)) - (discounted_strike * norm.cdf(d2))

    return (discounted_strike * norm.cdf(-d2)) - (spot_price * norm.cdf(-d1))
