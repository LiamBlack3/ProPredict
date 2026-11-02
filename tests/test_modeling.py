import sys
from pathlib import Path

import pandas as pd
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from modeling import compare_models, evaluate_and_forecast, yearly_series  # noqa: E402


def _series() -> pd.DataFrame:
    years = list(range(2000, 2022))
    return pd.DataFrame({"YEAR": years, "PTS": [90 + 0.8 * (y - 2000) for y in years]})


def test_yearly_series_averages_panel():
    df = pd.DataFrame(
        {
            "YEAR": [2020, 2020, 2021, 2021],
            "TEAM": ["A", "B", "A", "B"],
            "PTS": [100, 110, 102, 112],
        }
    )
    series = yearly_series(df, "PTS")
    assert list(series["YEAR"]) == [2020, 2021]
    assert series.loc[series["YEAR"] == 2020, "PTS"].iloc[0] == 105


def test_linear_forecast_follows_trend():
    result = evaluate_and_forecast(_series(), "PTS", "Linear Regression", 2021)
    assert result.n_train == 21
    assert result.forecast_year == 2022
    assert 106 < result.prediction < 109
    assert result.mae is not None
    assert result.mae < 1.0


def test_compare_models_returns_three_rows():
    table = compare_models(_series(), "PTS", 2021)
    assert set(table["model_name"]) == {
        "Linear Regression",
        "Ridge",
        "Random Forest",
    }


def test_too_few_seasons_raises():
    tiny = pd.DataFrame({"YEAR": [2019, 2020], "PTS": [100, 101]})
    with pytest.raises(ValueError):
        evaluate_and_forecast(tiny, "PTS", "Linear Regression", 2020)
