"""
AAYAM - Application Configuration
Paths, defaults, and environmental settings.
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REFERENCE_DATA_DIR = DATA_DIR / "reference"
MODELS_DIR = BASE_DIR / "models"
DOCS_DIR = BASE_DIR / "docs"

# Application Metadata
APP_NAME = "AAYAM"
APP_TITLE = "AAYAM — AI-Driven Multi-Dimensional Economic Mobility & Cyber-Financial Intelligence"
APP_TAGLINE = "See Every Dimension of Economic Opportunity."
SDG_ALIGNMENT = ["SDG 1 — No Poverty", "SDG 8 — Decent Work and Economic Growth"]

# Financial Engine Thresholds (Simplified Decision-Support Benchmarks)
RECOMMENDED_EMERGENCY_MONTHS = 6.0
MAX_RECOMMENDED_DTI_RATIO = 0.40  # 40% of take-home pay
HEALTHY_SAVINGS_RATE = 0.20        # 20% savings target

# Theme Color Constants
COLOR_BG = "#090D16"
COLOR_PRIMARY_SURFACE = "#0F172A"
COLOR_SECONDARY_SURFACE = "#1E293B"
COLOR_BORDER = "#334155"
COLOR_ACCENT_PRIMARY = "#10B981"  # Emerald
COLOR_ACCENT_SECONDARY = "#6366F1"  # Indigo
COLOR_WARNING = "#F59E0B"  # Amber
COLOR_DANGER = "#F43F5E"  # Rose
COLOR_TEXT_LIGHT = "#F8FAFC"
COLOR_TEXT_MUTED = "#94A3B8"
