import numpy as np
from scipy.stats import norm

def calculate_theoretical_value(spot_price: float, strike: float, time_to_expiry: float, volatility: float, risk_free_rate: float) -> float:
    if time_to_expiry <= 1e-8 or volatility <= 1e-8:
        discounted_strike = strike * np.exp(-risk_free_rate * time_to_expiry)
        return max(spot_price - discounted_strike, 0)
        
    sqrt_t = time_to_expiry ** 0.5

    d1 = (np.log(spot_price / strike) + (risk_free_rate + (volatility ** 2) / 2) * time_to_expiry) / (volatility * sqrt_t)
    d2 = d1 - volatility * sqrt_t

    return (spot_price * norm.cdf(d1)) - (strike * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2))