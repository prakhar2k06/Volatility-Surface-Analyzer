import numpy as np
import pandas as pd
from computation.black_scholes import calculate_theoretical_value

VOL_MIN = 0.05
VOL_MAX = 1.50

def synthetic_volatility_generator(
    s: float, 
    k: float, 
    t: float, 
    ATM_VOL: float = 0.18, 
    ATM_VOL_BUMP: float = 0.08, 
    ATM_DECAY: float = 0.5, 
    SKEW_STRENGTH: float = -0.30, 
    SKEW_DECAY: float = 0.6, 
    SMILE_STRENGTH: float = 0.60,
    SMILE_DECAY: float = 1.20,) -> float:
    '''
    Generates a synthetic volatility given various parameters such as decay. Used to generate synthetic market prices.
    '''
    moneyness = np.log(k / s)

    base = ATM_VOL + ATM_VOL_BUMP * np.exp(-t / ATM_DECAY)
    skew = SKEW_STRENGTH * np.exp(-t / SKEW_DECAY)
    smile = SMILE_STRENGTH * np.exp(-t/SMILE_DECAY)
    
    volatility = base + (skew * moneyness) + (smile * (moneyness**2))

    return np.clip(volatility, VOL_MIN, VOL_MAX)

def generate_market_prices(
    spot: float, 
    strikes: np.ndarray, 
    maturities: np.ndarray, 
    rate: float, 
    noise_amt: float = 0,
    ATM_VOL: float = 0.18, 
    ATM_VOL_BUMP: float = 0.08, 
    ATM_DECAY: float = 0.5, 
    SKEW_STRENGTH: float = -0.30, 
    SKEW_DECAY: float = 0.6, 
    SMILE_STRENGTH: float = 0.60,
    SMILE_DECAY: float = 1.20):
    '''
    Generates synthetic market prices dataframe, used as ground truth. This pipeline can be modified to use real market data.
    '''
    market_prices = pd.DataFrame(index=strikes, columns=maturities, dtype=float)
    true_vol = pd.DataFrame(index=strikes, columns=maturities, dtype=float)

    for strike in strikes:
        for maturity in maturities:
            vol = synthetic_volatility_generator(spot, strike, maturity, ATM_VOL, ATM_VOL_BUMP, ATM_DECAY, SKEW_STRENGTH, SKEW_DECAY, SMILE_STRENGTH, SMILE_DECAY)
            noise = np.random.normal(0.0, noise_amt) if noise_amt > 0 else 0.0
            price = calculate_theoretical_value(spot, strike, maturity, vol, rate) * (1 + noise)
            market_prices.loc[strike, maturity] = price
            true_vol.loc[strike, maturity] = vol

    return market_prices, true_vol
            


