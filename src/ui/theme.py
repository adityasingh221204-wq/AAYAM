"""
AAYAM - Modern Fintech Theme & Custom CSS
Implements clean card layouts, dark surface contrast, and accessible typography.
"""
import streamlit as st
from src.utils.config import (
    COLOR_BG, COLOR_PRIMARY_SURFACE, COLOR_SECONDARY_SURFACE,
    COLOR_BORDER, COLOR_ACCENT_PRIMARY, COLOR_ACCENT_SECONDARY,
    COLOR_WARNING, COLOR_DANGER, COLOR_TEXT_LIGHT, COLOR_TEXT_MUTED
)


def apply_theme():
    """Inject custom CSS for consistent fintech styling across all pages."""
    css = f"""
    <style>
    /* Main Background & Font Hierarchy */
    .stApp {{
        background-color: {COLOR_BG};
        color: {COLOR_TEXT_LIGHT};
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    
    /* Top Header Bar */
    header[data-testid="stHeader"] {{
        background-color: {COLOR_BG};
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {COLOR_PRIMARY_SURFACE};
        border-right: 1px solid {COLOR_BORDER};
    }}
    
    /* Card Container */
    .aayam-card {{
        background-color: {COLOR_PRIMARY_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
    }}
    
    .aayam-card-secondary {{
        background-color: {COLOR_SECONDARY_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }}
    
    /* KPI Metric Cards */
    .kpi-container {{
        background: linear-gradient(145deg, {COLOR_PRIMARY_SURFACE}, {COLOR_SECONDARY_SURFACE});
        border: 1px solid {COLOR_BORDER};
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        flex-direction: column;
        justify_content: space-between;
    }}
    
    .kpi-title {{
        color: {COLOR_TEXT_MUTED};
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }}
    
    .kpi-value {{
        color: {COLOR_TEXT_LIGHT};
        font-size: 1.65rem;
        font-weight: 700;
        margin-bottom: 4px;
        letter-spacing: -0.02em;
    }}
    
    .kpi-subtext {{
        color: {COLOR_TEXT_MUTED};
        font-size: 0.80rem;
    }}
    
    /* Badges & Status Pills */
    .badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }}
    
    .badge-emerald {{
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    
    .badge-indigo {{
        background-color: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }}
    
    .badge-amber {{
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    
    .badge-rose {{
        background-color: rgba(244, 63, 94, 0.15);
        color: #FB7185;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }}
    
    /* Form inputs and buttons */
    .stButton>button {{
        background-color: {COLOR_ACCENT_PRIMARY};
        color: #090D16;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 8px 18px;
        transition: all 0.2s ease;
    }}
    
    .stButton>button:hover {{
        background-color: #059669;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }}
    
    /* Data Provenance Note Box */
    .provenance-box {{
        background-color: rgba(30, 41, 59, 0.6);
        border-left: 3px solid {COLOR_ACCENT_SECONDARY};
        padding: 10px 14px;
        border-radius: 4px;
        font-size: 0.78rem;
        color: {COLOR_TEXT_MUTED};
        margin-top: 14px;
    }}
    
    /* Student Prototype Disclaimer Footer */
    .aayam-footer {{
        border-top: 1px solid {COLOR_BORDER};
        padding-top: 16px;
        margin-top: 40px;
        font-size: 0.78rem;
        color: {COLOR_TEXT_MUTED};
        text-align: center;
        line-height: 1.5;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
