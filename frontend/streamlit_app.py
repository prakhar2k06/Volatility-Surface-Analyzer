import plotly.io as pio
import requests
import streamlit as st
from pydantic import BaseModel

BACKEND_URL = "http://127.0.0.1:8000"


class TickerResponse(BaseModel):
    ticker: str
    quality_report: dict
    raw_surface: str | None
    smoothed_surface: str | None
    smile: str | None
    term_structure: str | None


st.set_page_config(
    page_title="Volatility Surface Analyzer",
    layout="wide",
)


if "ticker_data" not in st.session_state:
    st.session_state.ticker_data = None

if "last_ticker" not in st.session_state:
    st.session_state.last_ticker = None


with st.sidebar:
    st.markdown(
        """
        <h1 style='margin-bottom: 0.25rem;'>Volatility Surface Analyzer</h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Input")

    ticker_input: str = st.text_input(
        "Ticker",
        placeholder="TSLA",
    )

    submitted: bool = st.button("Analyze", use_container_width=True)

    st.markdown("---")
    st.markdown("### Display")

    plot_choice: str = st.radio(
        "Select plot",
        options=[
            "Smoothed IV Surface",
            "Raw IV Surface",
            "Term Structure",
            "Smile",
        ],
        index=0,
    )

    st.markdown("<div style='height: 240px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <p style='font-size: 0.8rem; color: gray; line-height: 1.3;'>
            <em>Data sourced from yfinance may be sparse or stale.</em>
        </p>
        """,
        unsafe_allow_html=True,
    )

if submitted:
    ticker: str = ticker_input.upper().strip()

    if not ticker:
        st.warning("Please enter a ticker.")
        st.stop()

    if st.session_state.ticker_data is None or st.session_state.last_ticker != ticker:
        payload: dict[str, str] = {"ticker": ticker}

        try:
            with st.spinner(f"Analyzing {ticker}..."):
                response = requests.post(
                    f"{BACKEND_URL}/volatility-surface",
                    json=payload,
                    timeout=120,
                )

            if response.status_code != 200:
                try:
                    detail = response.json().get("detail", "Backend error")
                except Exception:
                    detail = response.text

                st.error(detail)
                st.stop()

            data = response.json()
            structured_data = TickerResponse(**data)

            st.session_state.ticker_data = structured_data
            st.session_state.last_ticker = ticker

        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the backend server. Is FastAPI active?")
            st.stop()

        except requests.exceptions.Timeout:
            st.error("The backend took too long to respond.")
            st.stop()

        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.stop()


structured_data = st.session_state.ticker_data

if structured_data is None:
    st.info("Enter a ticker in the sidebar and click Analyze.")
else:
    st.markdown(f"## {structured_data.ticker}")

    plot_map = {
        "Smoothed IV Surface": structured_data.smoothed_surface,
        "Raw IV Surface": structured_data.raw_surface,
        "Term Structure": structured_data.term_structure,
        "Smile": structured_data.smile,
    }

    selected_plot: str | None = plot_map[plot_choice]

    if selected_plot is None:
        st.warning(f"{plot_choice} is not available for this ticker.")
    else:
        st.markdown(f"### {plot_choice}")
        fig = pio.from_json(selected_plot)

        fig.update_layout(title={"text": ""})

        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Data Quality Report", expanded=False):
        st.json(structured_data.quality_report)
