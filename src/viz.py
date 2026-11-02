"""Plotly charts used by the Streamlit app."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

from modeling import ForecastResult


def scatter_with_trend(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None,
    hover_name: str | None,
    hover_data: list[str] | None = None,
) -> go.Figure:
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        trendline="ols",
        trendline_color_override="#2E7D32",
        hover_name=hover_name,
        hover_data=hover_data,
    )
    fig.update_layout(legend_title_text=color or "", margin=dict(l=10, r=10, t=40, b=10))
    return fig


def ols_summary(x: pd.Series, y: pd.Series) -> dict[str, float]:
    paired = pd.concat([x, y], axis=1).dropna()
    if len(paired) < 3:
        return {}
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        paired.iloc[:, 0], paired.iloc[:, 1]
    )
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r": float(r_value),
        "r_squared": float(r_value**2),
        "p_value": float(p_value),
        "std_err": float(std_err),
        "n": float(len(paired)),
    }


def add_forecast_marker(fig: go.Figure, result: ForecastResult) -> go.Figure:
    fig.add_trace(
        go.Scatter(
            x=[result.forecast_year],
            y=[result.prediction],
            mode="markers",
            name=f"{result.model_name} forecast",
            marker=dict(color="#C62828", size=12, symbol="diamond"),
        )
    )
    return fig
