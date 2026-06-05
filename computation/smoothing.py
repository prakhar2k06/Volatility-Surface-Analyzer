import pandas as pd
from scipy.ndimage import gaussian_filter


def surface_smoother(df: pd.DataFrame) -> pd.DataFrame:
    """
    Smoothens the volatility surface.

    Real market surfaces are sparse after pivoting, so missing values
    must be interpolated before applying Gaussian smoothing.
    """
    filled = df.interpolate(axis=0, limit_direction="both").interpolate(
        axis=1, limit_direction="both"
    )

    z = filled.values
    z_smooth = gaussian_filter(z, sigma=(1.3, 1.3))

    return pd.DataFrame(z_smooth, index=df.index, columns=df.columns)
