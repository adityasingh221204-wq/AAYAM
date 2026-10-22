"""
AAYAM - Data Validation Utilities
Validates DataFrames and user profile structures against required schemas.
"""
import pandas as pd
from src.data.schemas import SCHEMAS
from src.utils.logging_config import logger


def validate_dataframe(df: pd.DataFrame, schema_name: str) -> tuple[bool, list[str]]:
    """
    Validate a pandas DataFrame against a registered schema.
    Returns (is_valid, list_of_error_strings).
    """
    errors = []
    if df is None or df.empty:
        return False, ["DataFrame is empty or None."]
        
    if schema_name not in SCHEMAS:
        return True, [f"Warning: No explicit schema registered for '{schema_name}'."]
        
    schema = SCHEMAS[schema_name]
    required_cols = schema.get("required_columns", [])
    numeric_cols = schema.get("numeric_columns", [])
    
    # Check missing required columns
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns in '{schema_name}': {', '.join(missing_cols)}")
        
    # Check numeric columns conversion
    for num_col in numeric_cols:
        if num_col in df.columns:
            non_null_vals = df[num_col].dropna()
            if not non_null_vals.empty:
                converted = pd.to_numeric(non_null_vals, errors="coerce")
                nan_count = converted.isna().sum()
                if nan_count > 0:
                    errors.append(f"Column '{num_col}' contains {nan_count} non-numeric values.")
                    
    is_valid = len(errors) == 0
    return is_valid, errors


def validate_financial_profile(profile: dict) -> tuple[bool, list[str]]:
    """
    Validate user financial profile dictionary.
    Ensures sensible non-negative numeric entries and safe defaults.
    """
    errors = []
    if not isinstance(profile, dict):
        return False, ["Profile must be a dictionary."]
        
    numeric_fields = [
        "monthly_take_home_income",
        "other_monthly_income",
        "essential_monthly_expenses",
        "discretionary_expenses",
        "current_savings",
        "outstanding_debt",
        "monthly_debt_repayments",
        "emergency_expenses_obligations"
    ]
    
    for field in numeric_fields:
        if field in profile:
            val = profile[field]
            if val is not None:
                try:
                    num_val = float(val)
                    if num_val < 0:
                        errors.append(f"Field '{field}' cannot be negative ({num_val}).")
                except (ValueError, TypeError):
                    errors.append(f"Field '{field}' must be a valid number, got {type(val).__name__}.")
                    
    return len(errors) == 0, errors
