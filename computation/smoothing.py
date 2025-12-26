from scipy.ndimage import gaussian_filter
import pandas as pd

def surface_smoother(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Helper function that smoothens the volatility surface for better understanding.
    '''
    z = df.values
    z_smooth = gaussian_filter(z, (1.0, 1.0))
    return pd.DataFrame(z_smooth, index = df.index, columns = df.columns)
