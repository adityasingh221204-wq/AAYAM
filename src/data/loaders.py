"""
AAYAM - Public Dataset Loaders
Implements the canonical loader contract:
    load_public_dataset(dataset_name: str, data_dir: str | None = None) -> pandas.DataFrame
Handles missing files, schema mapping, and returns clean, validated DataFrames.
"""
import os
from pathlib import Path
import pandas as pd
from src.utils.logging_config import logger
from src.data.validators import validate_dataframe

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DATA_DIR = BASE_DIR / "data"

# Canonical dataset name mapping to relative processed/reference paths and schema names
DATASET_REGISTRY = {
    "rbi_payment_systems": {
        "rel_path": "processed/rbi/payment_systems_monthly.csv",
        "schema": "payment_systems",
        "aliases": ["rbi", "payments", "payment_systems"]
    },
    "domestic_payment_frauds": {
        "rel_path": "processed/rbi/domestic_payment_frauds.csv",
        "schema": "domestic_payment_frauds",
        "aliases": ["frauds", "rbi_frauds", "payment_frauds"]
    },
    "plfs_indicators": {
        "rel_path": "processed/plfs/plfs_indicators_2023_24.csv",
        "schema": "plfs_indicators",
        "aliases": ["plfs", "labour", "employment"]
    },
    "hces_indicators": {
        "rel_path": "processed/hces/hces_indicators_2023_24.csv",
        "schema": "hces_indicators",
        "aliases": ["hces", "consumption", "expenditure"]
    },
    "asuse_indicators": {
        "rel_path": "processed/asuse/asuse_indicators_2023_24.csv",
        "schema": "asuse_indicators",
        "aliases": ["asuse", "enterprises", "msme"]
    },
    "cert_in_advisories": {
        "rel_path": "processed/cyber_threats/cert_in_advisories.csv",
        "schema": "cert_in_advisories",
        "aliases": ["cert_in", "threats", "cyber_advisories"]
    },
    "opportunities": {
        "rel_path": "processed/opportunities/opportunity_catalogue.csv",
        "schema": "opportunities",
        "aliases": ["opportunity_catalogue", "jobs", "pathways"]
    },
    "source_register": {
        "rel_path": "reference/source_register.csv",
        "schema": "source_register",
        "aliases": ["sources", "register"]
    },
    "geography_mapping": {
        "rel_path": "reference/geography_mapping.csv",
        "schema": "geography",
        "aliases": ["geography", "states"]
    },
    "state_cyber_frauds": {
        "rel_path": "processed/cyber_threats/state_cyber_fraud_statistics.csv",
        "schema": "state_cyber_frauds",
        "aliases": ["ncrp_frauds", "1930_stats", "state_frauds", "cyber_crime_states"]
    },
    "upi_app_ecosystem": {
        "rel_path": "processed/rbi/upi_app_ecosystem.csv",
        "schema": "upi_app_ecosystem",
        "aliases": ["upi_apps", "npci_apps", "upi_market_share"]
    }
}


def _resolve_canonical_key(dataset_name: str) -> str | None:
    """Resolve alias or key to canonical registry key."""
    clean_name = dataset_name.strip().lower().replace("-", "_").replace(" ", "_")
    if clean_name in DATASET_REGISTRY:
        return clean_name
    for canonical_key, meta in DATASET_REGISTRY.items():
        if clean_name in meta["aliases"]:
            return canonical_key
    return None


def load_public_dataset(dataset_name: str, data_dir: str | None = None) -> pd.DataFrame:
    """
    Canonical loader function.
    
    Args:
        dataset_name: Name or alias of the dataset (e.g. 'plfs', 'rbi_frauds', 'hces').
        data_dir: Optional custom base directory for data. Defaults to repo 'data/' folder.
        
    Returns:
        pandas.DataFrame: The loaded dataset, or an empty DataFrame if missing/unparseable.
    """
    canonical_key = _resolve_canonical_key(dataset_name)
    if not canonical_key:
        logger.warning(f"Unknown dataset name requested: '{dataset_name}'. Returning empty DataFrame.")
        return pd.DataFrame()
        
    meta = DATASET_REGISTRY[canonical_key]
    base_path = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    target_path = base_path / meta["rel_path"]
    
    if not target_path.exists():
        logger.warning(f"Dataset file not found at: {target_path}. Returning empty DataFrame.")
        return pd.DataFrame()
        
    try:
        if target_path.suffix.lower() == ".csv":
            df = pd.read_csv(target_path)
        elif target_path.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(target_path)
        elif target_path.suffix.lower() == ".json":
            df = pd.read_json(target_path)
        else:
            logger.error(f"Unsupported file format for dataset: {target_path}")
            return pd.DataFrame()
            
        # Validate against schema
        is_valid, errors = validate_dataframe(df, meta["schema"])
        if not is_valid:
            logger.warning(f"Validation warnings for '{dataset_name}': {'; '.join(errors)}")
            
        return df
        
    except Exception as e:
        logger.error(f"Error loading dataset '{dataset_name}' from {target_path}: {e}")
        return pd.DataFrame()
