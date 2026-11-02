"""ProPredict: interactive NBA exploration and baseline trend forecasting."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import pandas as pd
import streamlit as st

from data_io import (
    filter_selection,
    load_csv,
    load_sample_player,
    load_sample_team,
    numeric_columns,
    require_columns,
    year_bounds,
)
from modeling import MODEL_CHOICES, compare_models, evaluate_and_forecast, yearly_series
from viz import add_forecast_marker, ols_summary, scatter_with_trend

ALL_TEAMS = "All Teams"


@st.cache_data(show_spinner=False)
def _cached_sample_team() -> pd.DataFrame:
    return load_sample_team()


@st.cache_data(show_spinner=False)
def _cached_sample_player() -> pd.DataFrame:
    return load_sample_player()


def page_config() -> None:
    st.set_page_config(
        page_title="ProPredict | NBA Analytics",
        page_icon="🏀",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def load_datasets():
    st.sidebar.header("Data")
    use_sample = st.sidebar.toggle("Use bundled NBA sample data", value=True)
    team_upload = st.sidebar.file_uploader("Team season CSV", type=["csv"], key="team_csv")
    player_upload = st.sidebar.file_uploader("Player season CSV", type=["csv"], key="player_csv")

    team_df = player_df = None
    errors = []

    try:
        if team_upload is not None:
            team_df = load_csv(team_upload)
            require_columns(team_df, ("YEAR", "TEAM"), "Team")
        elif use_sample:
            team_df = _cached_sample_team()
    except (ValueError, OSError, pd.errors.ParserError) as exc:
        errors.append(str(exc))

    try:
        if player_upload is not None:
            player_df = load_csv(player_upload)
            require_columns(player_df, ("YEAR", "TEAM", "Player"), "Player")
        elif use_sample:
            player_df = _cached_sample_player()
    except (ValueError, OSError, pd.errors.ParserError) as exc:
        errors.append(str(exc))

    for message in errors:
        st.sidebar.error(message)
    return team_df, player_df


def home_page() -> None:
    st.title("ProPredict")
    st.subheader("Interactive NBA analysis with transparent trend forecasts")
    st.write(
        "ProPredict is a Streamlit app for exploring NBA team and player season "
        "statistics, measuring associations, and producing a next-season forecast "
        "from a year-based baseline model."
    )
    left, right = st.columns(2)
    with left:
        st.markdown(
            """
            **What you can do**
            - Inspect team and player tables, missingness, and distributions
            - Plot any numeric pairing with an OLS trendline
            - Compare linear, ridge, and random forest trend models
            - Score models on a held-out season before forecasting the next year
            """
        )
    with right:
        st.markdown(
            """
            **How forecasting works**
            - Feature: season year only
            - Split: train on seasons before the holdout year
            - Report: MAE / RMSE on the holdout season, then a one-year-ahead point forecast
            - Caveat: this is a trend baseline, not a multi-factor player projection
            """
        )


def data_summary(team_df: pd.DataFrame | None, player_df: pd.DataFrame | None) -> None:
    st.title("Data summary")
    if team_df is None and player_df is None:
        st.info("Load team or player data from the sidebar to continue.")
        return

    if team_df is not None:
        st.header("Teams")
        _summary_block(team_df)
    if player_df is not None:
        st.header("Players")
        _summary_block(player_df)


def _summary_block(df: pd.DataFrame) -> None:
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", f"{df.shape[1]}")
    if "YEAR" in df.columns:
        lo, hi = year_bounds(df)
        c3.metric("Seasons", f"{lo}–{hi}")
    st.dataframe(df.head(50), use_container_width=True)
    with st.expander("Descriptive statistics"):
        st.dataframe(df.describe(include="number").T, use_container_width=True)
    missing = df.isna().mean().sort_values(ascending=False)
    missing = missing[missing > 0]
    if not missing.empty:
        with st.expander("Share of missing values"):
            st.dataframe(missing.rename("missing_rate").to_frame(), use_container_width=True)


def _metric_cards(summary: dict) -> None:
    if not summary:
        st.warning("Need at least three paired observations to estimate OLS.")
        return
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("R²", f"{summary['r_squared']:.3f}")
    c2.metric("Slope", f"{summary['slope']:.3f}")
    c3.metric("p-value", f"{summary['p_value']:.3g}")
    c4.metric("n", f"{int(summary['n'])}")


def interactive_plots(team_df: pd.DataFrame | None, player_df: pd.DataFrame | None) -> None:
    st.title("Interactive plots")
    st.caption("OLS trendlines describe association in the selected sample. They are not forecasts.")
    tab_team, tab_player = st.tabs(["Team", "Player"])

    with tab_team:
        if team_df is None:
            st.info("Upload or enable sample team data.")
        else:
            _team_plot(team_df)
    with tab_player:
        if player_df is None:
            st.info("Upload or enable sample player data.")
        else:
            _player_plot(player_df, key_prefix="explore_player")


def _team_selector(df: pd.DataFrame, key: str) -> pd.DataFrame:
    teams = sorted(df["TEAM"].dropna().unique().tolist())
    selected = st.multiselect("Teams", [ALL_TEAMS] + teams, default=[ALL_TEAMS], key=f"{key}_teams")
    return filter_selection(df, "TEAM", selected, ALL_TEAMS)


def _team_plot(df: pd.DataFrame) -> None:
    filtered = _team_selector(df, "explore_team")
    if filtered.empty:
        st.warning("Select at least one team.")
        return
    nums = numeric_columns(filtered)
    if len(nums) < 2:
        st.warning("Need at least two numeric columns.")
        return
    c1, c2 = st.columns(2)
    x_col = c1.selectbox("X axis", nums, index=nums.index("YEAR") if "YEAR" in nums else 0, key="team_x")
    y_default = nums.index("PTS") if "PTS" in nums else min(1, len(nums) - 1)
    y_col = c2.selectbox("Y axis", nums, index=y_default, key="team_y")
    fig = scatter_with_trend(
        filtered, x_col, y_col, color="TEAM", hover_name="TEAM", hover_data=["YEAR"]
    )
    _metric_cards(ols_summary(filtered[x_col], filtered[y_col]))
    st.plotly_chart(fig, use_container_width=True)


def _player_plot(df: pd.DataFrame, key_prefix: str) -> pd.DataFrame | None:
    filtered = _team_selector(df, key_prefix)
    if filtered.empty:
        st.warning("Select at least one team.")
        return None
    players = sorted(filtered["Player"].dropna().unique().tolist())
    player = st.selectbox("Player", players, key=f"{key_prefix}_player")
    player_df = filtered[filtered["Player"] == player]
    nums = numeric_columns(player_df)
    if len(nums) < 2:
        st.warning("Need at least two numeric columns.")
        return None
    c1, c2 = st.columns(2)
    x_col = c1.selectbox("X axis", nums, index=nums.index("YEAR") if "YEAR" in nums else 0, key=f"{key_prefix}_x")
    y_default = nums.index("PTS") if "PTS" in nums else min(1, len(nums) - 1)
    y_col = c2.selectbox("Y axis", nums, index=y_default, key=f"{key_prefix}_y")
    fig = scatter_with_trend(
        player_df, x_col, y_col, color="TEAM", hover_name="Player", hover_data=["TEAM", "YEAR"]
    )
    _metric_cards(ols_summary(player_df[x_col], player_df[y_col]))
    st.plotly_chart(fig, use_container_width=True)
    return player_df


def predictive_modeling(team_df: pd.DataFrame | None, player_df: pd.DataFrame | None) -> None:
    st.title("Predictive modeling")
    st.caption(
        "Models forecast the selected statistic from season year. "
        "Holdout metrics are computed on a later season that was not used for fitting."
    )
    tab_team, tab_player = st.tabs(["Team forecast", "Player forecast"])
    with tab_team:
        if team_df is None:
            st.info("Upload or enable sample team data.")
        else:
            _forecast_panel(team_df, entity="team")
    with tab_player:
        if player_df is None:
            st.info("Upload or enable sample player data.")
        else:
            _forecast_panel(player_df, entity="player")

    with st.expander("Method notes"):
        st.markdown(
            """
            - **Target construction:** if multiple teams are selected, the model uses the
              seasonal mean of the chosen statistic so the series is one point per year.
            - **Validation:** seasons strictly before the holdout year are the training set.
            - **Linear / Ridge:** parametric trend. Ridge is a regularized linear baseline.
            - **Random forest:** nonlinear trend with conservative depth because yearly
              samples are small. It can still overfit; prefer holdout MAE over training fit.
            - **Limitation:** year is a proxy for era, rule changes, and aging. Use this as
              an exploratory baseline, not as a front-office projection system.
            """
        )


def _forecast_panel(df: pd.DataFrame, entity: str) -> None:
    filtered = _team_selector(df, f"pred_{entity}")
    if entity == "player":
        players = sorted(filtered["Player"].dropna().unique().tolist())
        if not players:
            st.warning("No players in the current filter.")
            return
        player = st.selectbox("Player", players, key=f"pred_{entity}_player")
        filtered = filtered[filtered["Player"] == player]

    nums = numeric_columns(filtered, extra_exclude=("YEAR",))
    if not nums:
        st.warning("No numeric targets available.")
        return
    y_default = nums.index("PTS") if "PTS" in nums else 0
    target = st.selectbox("Statistic to forecast", nums, index=y_default, key=f"pred_{entity}_y")
    model_name = st.selectbox("Model", MODEL_CHOICES, key=f"pred_{entity}_model")

    series = yearly_series(filtered, target)
    if series.empty or series["YEAR"].nunique() < 4:
        st.warning("Need at least four seasons of the selected statistic.")
        return

    min_year, max_year = int(series["YEAR"].min()), int(series["YEAR"].max())
    default_holdout = max_year
    holdout = st.slider(
        "Holdout season",
        min_value=min_year + 3,
        max_value=max_year,
        value=default_holdout,
        key=f"pred_{entity}_holdout",
    )

    try:
        result = evaluate_and_forecast(series, target, model_name, holdout)
    except ValueError as exc:
        st.error(str(exc))
        return

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(f"Forecast {result.forecast_year}", f"{result.prediction:.2f}")
    m2.metric("Holdout MAE", "n/a" if result.mae is None else f"{result.mae:.2f}")
    m3.metric("Holdout RMSE", "n/a" if result.rmse is None else f"{result.rmse:.2f}")
    m4.metric("Training seasons", str(result.n_train))

    fig = scatter_with_trend(
        filtered,
        "YEAR",
        target,
        color="TEAM" if entity == "team" else "Player",
        hover_name="TEAM" if entity == "team" else "Player",
        hover_data=["YEAR"],
    )
    st.plotly_chart(add_forecast_marker(fig, result), use_container_width=True)
    st.caption(
        "The red diamond is the one-year-ahead forecast of the seasonal mean. "
        "Scatter points are the underlying team or player rows."
    )

    st.subheader("Model comparison on the same split")
    comparison = compare_models(series, target, holdout)
    display = comparison.copy()
    for col in ("mae", "rmse", "r2", "prediction"):
        if col in display.columns:
            display[col] = display[col].map(lambda v: None if pd.isna(v) else round(float(v), 3))
    st.dataframe(display, use_container_width=True, hide_index=True)


def main() -> None:
    page_config()
    team_df, player_df = load_datasets()
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Page",
        ["Home", "Data summary", "Interactive plots", "Predictive modeling"],
        label_visibility="collapsed",
    )
    if page == "Home":
        home_page()
    elif page == "Data summary":
        data_summary(team_df, player_df)
    elif page == "Interactive plots":
        interactive_plots(team_df, player_df)
    else:
        predictive_modeling(team_df, player_df)


if __name__ == "__main__":
    main()
