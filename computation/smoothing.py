from scipy.ndimage import gaussian_filter
import pandas as pd

def surface_smoother(df: pd.DataFrame) -> pd.DataFrame:
    z = df.values
    z_smooth = gaussian_filter(z, (1.5, 1.5))
    return pd.DataFrame(z_smooth, index = df.index, columns = df.columns)
