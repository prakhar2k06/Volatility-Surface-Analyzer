from fastapi import FastAPI, HTTPException
from pandas import DataFrame
from pydantic import BaseModel

from computation.implied_volatility import calculate_implied_volatility_df
from computation.smoothing import surface_smoother
from data.cleaner import clean_option_chain
from data.fetcher import fetch_option_chain
from visualization.smile import plot_smile
from visualization.surface_prep import prepare_surface_grid
from visualization.term_structure import plot_term_structure
from visualization.volatility_surface import plot_volatility_surface

app = FastAPI()


class TickerRequest(BaseModel):
    ticker: str


class TickerResponse(BaseModel):
    ticker: str
    quality_report: dict
    raw_surface: str | None
    smoothed_surface: str | None
    smile: str | None
    term_structure: str | None


@app.post("/volatility-surface", response_model=TickerResponse)
def process_request(request: TickerRequest) -> TickerResponse:
    try:
        raw_df: DataFrame = fetch_option_chain(request.ticker)

        clean_df, report = clean_option_chain(raw_df)

        iv_df: DataFrame = calculate_implied_volatility_df(clean_df)

        plotting_df = prepare_surface_grid(iv_df)
        smoothed_df = surface_smoother(plotting_df)

        spot = float(iv_df["spot_price"].iloc[0])

        raw_plot = plot_volatility_surface(
            plotting_df,
            title="Implied Volatility Surface",
        )

        smooth_plot = plot_volatility_surface(
            smoothed_df,
            title="Smoothed Implied Volatility Surface",
        )

        smile_plot = plot_smile(
            smoothed_df,
            title="Volatility Smile",
        )

        term_structure_plot = plot_term_structure(
            smoothed_df,
            spot=spot,
            title="Volatility Term Structure",
        )

        return TickerResponse(
            ticker=request.ticker.upper().strip(),
            quality_report=report,
            raw_surface=raw_plot.to_json(),
            smoothed_surface=smooth_plot.to_json(),
            smile=smile_plot.to_json(),
            term_structure=term_structure_plot.to_json(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
