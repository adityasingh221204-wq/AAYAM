"""
AAYAM - Data Schemas & Expected Column Definitions
Defines required columns and types for incoming data tables.
"""

SCHEMAS = {
    "payment_systems": {
        "required_columns": ["system_name", "period", "volume_lakh", "value_inr_crore"],
        "numeric_columns": ["volume_lakh", "volume_crore", "value_inr_crore", "average_ticket_size_inr"]
    },
    "domestic_payment_frauds": {
        "required_columns": ["month_year", "fraud_volume_lakh", "fraud_value_inr_crore", "fts_basis_points"],
        "numeric_columns": ["fraud_volume_lakh", "fraud_incidents_count", "fraud_value_inr_crore", "fraud_incidence_1_in_x_transactions", "fts_basis_points"]
    },
    "plfs_indicators": {
        "required_columns": ["state", "sector", "gender", "lfpr_pct", "wpr_pct", "ur_pct"],
        "numeric_columns": ["lfpr_pct", "wpr_pct", "ur_pct", "avg_daily_earnings_regular_inr", "avg_daily_earnings_casual_inr"]
    },
    "hces_indicators": {
        "required_columns": ["sector", "fractile_class", "mpce_inr", "food_expenditure_share_pct", "non_food_share_pct"],
        "numeric_columns": ["mpce_inr", "food_expenditure_share_pct", "cereal_share_pct", "non_food_share_pct", "discretionary_expenditure_share_pct"]
    },
    "asuse_indicators": {
        "required_columns": ["broad_activity", "enterprise_type", "annual_gva_per_enterprise_inr"],
        "numeric_columns": ["annual_gva_per_enterprise_inr", "avg_workers_per_ent", "pct_share_enterprises", "avg_annual_emoluments_hired_worker_inr"]
    },
    "cert_in_advisories": {
        "required_columns": ["advisory_id", "title", "category", "attack_vector", "mitigation_steps"],
        "numeric_columns": []
    },
    "opportunities": {
        "required_columns": ["opportunity_id", "title", "track", "sector", "required_skills", "estimated_monthly_income_min_inr"],
        "numeric_columns": ["estimated_monthly_income_min_inr", "estimated_monthly_income_max_inr", "training_duration_weeks", "training_cost_inr", "capital_required_inr"]
    },
    "source_register": {
        "required_columns": ["dataset_id", "dataset_name", "publisher", "official_source_url", "access_status", "preprocessing_status"],
        "numeric_columns": ["file_size_bytes"]
    }
}
