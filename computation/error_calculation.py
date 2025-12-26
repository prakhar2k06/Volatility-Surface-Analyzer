import pandas as pd

def error_calculator(true_vol_surface: pd.DataFrame, implied_vol_surface: pd.DataFrame) -> pd.DataFrame:
    '''
    Helper function that calculates error between the two surfaces and returns absolute value dataframe.
    '''
    error_surface = abs(true_vol_surface - implied_vol_surface)
    return error_surface


