"""Temporal trend models for a selected NBA statistic.

These models use season year as the sole predictor. That is a transparent
baseline for direction of travel, not a causal or multi-factor forecast.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_CHOICES = ("Linear Regression", "Ridge", "Random Forest")


@dataclass
class ForecastResult:
    model_name: str
    holdout_year: int
    forecast_year: int
    prediction: float
    n_train: int
    n_holdout: int
    mae: float | None
    rmse: float | None
    r2: float | None

    def metrics_table(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(self)])


def yearly_series(df: pd.DataFrame, target: str, year_col: str = "YEAR") -> pd.DataFrame:
    """Collapse a panel to one value per season (mean of the selected rows)."""
    series = (
        df[[year_col, target]]
        .dropna()
        .groupby(year_col, as_index=False)[target]
        .mean()
        .sort_values(year_col)
    )
    return series


def _estimator(name: str, n_train: int):
    if name == "Linear Regression":
        return LinearRegression()
    if name == "Ridge":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", Ridge(alpha=1.0)),
            ]
        )
    leaf = 1 if n_train < 8 else 2
    depth = min(4, max(2, n_train // 3))
    return RandomForestRegressor(
        n_estimators=200,
        max_depth=depth,
        min_samples_leaf=leaf,
        random_state=42,
    )


def _xy(frame: pd.DataFrame, year_col: str, target: str):
    x = frame[[year_col]].to_numpy()
    y = frame[target].to_numpy()
    return x, y


def evaluate_and_forecast(
    series: pd.DataFrame,
    target: str,
    model_name: str,
    holdout_year: int,
    year_col: str = "YEAR",
) -> ForecastResult:
    if model_name not in MODEL_CHOICES:
        raise ValueError(f"Unknown model: {model_name}")
    if series.empty or target not in series.columns:
        raise ValueError("Not enough numeric data to fit a model.")

    train = series[series[year_col] < holdout_year]
    holdout = series[series[year_col] == holdout_year]
    if len(train) < 3:
        raise ValueError(
            "Need at least three seasons before the holdout year to fit a trend model."
        )

    model = _estimator(model_name, len(train))
    x_train, y_train = _xy(train, year_col, target)
    model.fit(x_train, y_train)

    mae = rmse = r2 = None
    if not holdout.empty:
        x_hold, y_hold = _xy(holdout, year_col, target)
        preds = model.predict(x_hold)
        mae = float(mean_absolute_error(y_hold, preds))
        rmse = float(np.sqrt(mean_squared_error(y_hold, preds)))
        r2 = float(r2_score(y_hold, preds)) if len(y_hold) > 1 else None

    forecast_year = int(series[year_col].max()) + 1
    prediction = float(model.predict(np.array([[forecast_year]]))[0])

    return ForecastResult(
        model_name=model_name,
        holdout_year=int(holdout_year),
        forecast_year=forecast_year,
        prediction=prediction,
        n_train=int(len(train)),
        n_holdout=int(len(holdout)),
        mae=mae,
        rmse=rmse,
        r2=r2,
    )


def compare_models(
    series: pd.DataFrame,
    target: str,
    holdout_year: int,
    year_col: str = "YEAR",
) -> pd.DataFrame:
    rows = []
    for name in MODEL_CHOICES:
        result = evaluate_and_forecast(series, target, name, holdout_year, year_col)
        rows.append(asdict(result))
    return pd.DataFrame(rows)
