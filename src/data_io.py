"""Load, validate, and prepare NBA team/player tables for the app."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
TEAM_SAMPLE = DATA_DIR / "nba_team_data.csv"
PLAYER_SAMPLE = DATA_DIR / "players.csv"

TEAM_ID_COLS = ("YEAR", "TEAM")
PLAYER_ID_COLS = ("YEAR", "TEAM", "Player")
CATEGORICAL_HINTS = {
    "TEAM",
    "Player",
    "Pos",
    "Player-additional",
}


def project_root() -> Path:
    return ROOT


def load_csv(source) -> pd.DataFrame:
    """Read a CSV from a path, uploaded file, or existing DataFrame."""
    if isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        df = pd.read_csv(source)
    return clean_frame(df)


def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    if "plus minus" in df.columns:
        df = df.rename(columns={"plus minus": "PLUS_MINUS"})
    if "YEAR" in df.columns:
        df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
        df = df.dropna(subset=["YEAR"])
        df["YEAR"] = df["YEAR"].astype(int)
    return df


def numeric_columns(df: pd.DataFrame, extra_exclude: tuple[str, ...] = ()) -> list[str]:
    exclude = set(CATEGORICAL_HINTS) | set(extra_exclude)
    cols = []
    for col in df.columns:
        if col in exclude:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            cols.append(col)
    return cols


def require_columns(df: pd.DataFrame, required: tuple[str, ...], label: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            f"{label} data is missing required columns: {', '.join(missing)}. "
            "Expected identifiers include YEAR and TEAM (and Player for player files)."
        )


def load_sample_team() -> pd.DataFrame:
    df = load_csv(TEAM_SAMPLE)
    require_columns(df, TEAM_ID_COLS, "Team")
    return df


def load_sample_player() -> pd.DataFrame:
    df = load_csv(PLAYER_SAMPLE)
    require_columns(df, PLAYER_ID_COLS, "Player")
    return df


def filter_selection(df: pd.DataFrame, column: str, selected: list[str], all_label: str) -> pd.DataFrame:
    if not selected or all_label in selected:
        return df.copy()
    return df[df[column].isin(selected)].copy()


def year_bounds(df: pd.DataFrame) -> tuple[int, int]:
    years = df["YEAR"].dropna()
    return int(years.min()), int(years.max())
