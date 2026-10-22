"""
AAYAM - Preprocessing & Normalization Utilities
"""
import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lower_snake_case safely."""
    df_clean = df.copy()
    df_clean.columns = [
        str(col).strip().lower().replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", "_")
        for col in df_clean.columns
    ]
    return df_clean


def safe_numeric_conversion(series: pd.Series, default: float = 0.0) -> pd.Series:
    """Convert a series to float with safe fill for NaNs."""
    return pd.to_numeric(series, errors="coerce").fillna(default)
