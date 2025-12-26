import numpy as np
from computation.black_scholes import calculate_theoretical_value

def calculate_implied_volatility(market_price: float, spot_price: float, strike: float, time_to_expiry: float, risk_free_rate: float, max_iter: int = 100, tol = 1e-6) -> float:
    '''
    Calculates implied volatility accurate to a certain tolerance using bisection root finder.
    '''
    if time_to_expiry <= 0 or market_price <= 0:
        return np.nan
    
    low = 1e-8
    high = 2
    
    for i in range(max_iter):
        mid = (low + high) / 2
        mid_price = calculate_theoretical_value(spot_price, strike, time_to_expiry, mid, risk_free_rate)

        error = mid_price - market_price

        if abs(error) < tol:
            return mid
        
        if error < 0:
            low = mid

        else:
            high = mid

    return np.nan






