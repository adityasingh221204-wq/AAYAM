"""
AAYAM - Modern Fintech Theme & Custom CSS
Premium dark-mode design system with glassmorphism, micro-animations,
smooth transitions, and responsive typography.
"""
import streamlit as st
from src.utils.config import (
    COLOR_BG, COLOR_PRIMARY_SURFACE, COLOR_SECONDARY_SURFACE,
    COLOR_BORDER, COLOR_ACCENT_PRIMARY, COLOR_ACCENT_SECONDARY,
    COLOR_WARNING, COLOR_DANGER, COLOR_TEXT_LIGHT, COLOR_TEXT_MUTED
)


def apply_theme():
    """Inject premium CSS for consistent fintech styling across all pages."""
    css = f"""
    <style>
    /* ── Import Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Entrance Animations ── */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(18px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    @keyframes pulse-glow {{
        0%, 100% {{ box-shadow: 0 0 8px rgba(16, 185, 129, 0.2); }}
        50% {{ box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); }}
    }}
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* ── Global App Foundation ── */
    .stApp {{
        background: linear-gradient(170deg, {COLOR_BG} 0%, #0C1220 40%, #0E1428 100%);
        color: {COLOR_TEXT_LIGHT};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        -webkit-font-smoothing: antialiased;
    }}

    /* ── Top Header Bar ── */
    header[data-testid="stHeader"] {{
        background: rgba(9, 13, 22, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(51, 65, 85, 0.3);
    }}

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLOR_PRIMARY_SURFACE} 0%, #0B1022 100%);
        border-right: 1px solid rgba(51, 65, 85, 0.4);
    }}
    section[data-testid="stSidebar"] .stMarkdown p {{
        font-size: 0.88rem;
    }}

    /* ── Primary Card Container (Glassmorphism) ── */
    .aayam-card {{
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(30, 41, 59, 0.55));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(51, 65, 85, 0.5);
        border-radius: 16px;
        padding: 22px 24px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.35), 0 4px 8px -4px rgba(0, 0, 0, 0.25);
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    border-color 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }}
    .aayam-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(129, 140, 248, 0.3), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    .aayam-card:hover {{
        transform: translateY(-4px);
        border-color: rgba(129, 140, 248, 0.4);
        box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.5), 0 8px 16px -4px rgba(99, 102, 241, 0.12);
    }}
    .aayam-card:hover::before {{
        opacity: 1;
    }}

    .aayam-card-secondary {{
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(6px);
        border: 1px solid rgba(51, 65, 85, 0.35);
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 12px;
        animation: fadeIn 0.4s ease-out;
    }}

    /* ── KPI Metric Cards ── */
    .kpi-container {{
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.5));
        border: 1px solid rgba(51, 65, 85, 0.45);
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 12px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.25s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.45s ease-out;
        position: relative;
        overflow: hidden;
    }}
    .kpi-container::after {{
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, {COLOR_ACCENT_PRIMARY}, transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    .kpi-container:hover {{
        transform: translateY(-2px);
        border-color: rgba(16, 185, 129, 0.35);
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.35);
    }}
    .kpi-container:hover::after {{
        opacity: 1;
    }}

    .kpi-title {{
        color: {COLOR_TEXT_MUTED};
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }}

    .kpi-value {{
        color: {COLOR_TEXT_LIGHT};
        font-size: 1.75rem;
        font-weight: 800;
        margin-bottom: 4px;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }}

    .kpi-subtext {{
        color: {COLOR_TEXT_MUTED};
        font-size: 0.78rem;
        line-height: 1.3;
    }}

    /* ── Badges & Status Pills ── */
    .badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        transition: transform 0.2s ease;
    }}
    .badge:hover {{
        transform: scale(1.05);
    }}

    .badge-emerald {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }}

    .badge-indigo {{
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(99, 102, 241, 0.1));
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.35);
    }}

    .badge-amber {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }}

    .badge-rose {{
        background: linear-gradient(135deg, rgba(244, 63, 94, 0.2), rgba(244, 63, 94, 0.1));
        color: #FB7185;
        border: 1px solid rgba(244, 63, 94, 0.35);
    }}

    /* ── Fit Tier Badges ── */
    .aayam-badge-tier {{
        display: inline-block;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}
    .aayam-badge-tier-high {{
        background: rgba(16, 185, 129, 0.18);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.45);
    }}
    .aayam-badge-tier-mod {{
        background: rgba(99, 102, 241, 0.18);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.45);
    }}
    .aayam-badge-tier-dev {{
        background: rgba(148, 163, 184, 0.18);
        color: #94A3B8;
        border: 1px solid rgba(148, 163, 184, 0.35);
    }}

    /* ── Custom Progress Bar ── */
    .aayam-progress-bar {{
        width: 100%;
        background: rgba(51, 65, 85, 0.5);
        border-radius: 9999px;
        height: 10px;
        overflow: hidden;
        margin: 8px 0;
    }}
    .aayam-progress-fill {{
        height: 100%;
        border-radius: 9999px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    /* ── Buttons (Premium) ── */
    .stButton>button {{
        background: linear-gradient(135deg, {COLOR_ACCENT_PRIMARY}, #059669);
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.88rem;
        border: none;
        border-radius: 10px;
        padding: 10px 22px;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #059669, {COLOR_ACCENT_PRIMARY});
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35);
        transform: translateY(-1px);
    }}
    .stButton>button:active {{
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.2);
    }}

    /* ── Data Provenance Box ── */
    .provenance-box {{
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(4px);
        border-left: 3px solid {COLOR_ACCENT_SECONDARY};
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        font-size: 0.78rem;
        color: {COLOR_TEXT_MUTED};
        margin-top: 14px;
        transition: border-color 0.3s ease;
    }}
    .provenance-box:hover {{
        border-left-color: {COLOR_ACCENT_PRIMARY};
    }}

    /* ── Footer ── */
    .aayam-footer {{
        border-top: 1px solid rgba(51, 65, 85, 0.4);
        padding-top: 20px;
        margin-top: 48px;
        font-size: 0.78rem;
        color: {COLOR_TEXT_MUTED};
        text-align: center;
        line-height: 1.6;
        animation: fadeIn 0.6s ease;
    }}

    /* ── Hero Section ── */
    .aayam-hero {{
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.4));
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 36px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }}
    .aayam-hero::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -30%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
        pointer-events: none;
    }}
    .aayam-hero::after {{
        content: '';
        position: absolute;
        bottom: -40%;
        left: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.06) 0%, transparent 70%);
        pointer-events: none;
    }}

    /* ── Module Navigation Cards ── */
    .module-card {{
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.4));
        backdrop-filter: blur(8px);
        border: 1px solid rgba(51, 65, 85, 0.4);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 14px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }}
    .module-card:hover {{
        transform: translateY(-3px) scale(1.005);
        border-color: rgba(129, 140, 248, 0.35);
        box-shadow: 0 12px 32px -6px rgba(0, 0, 0, 0.4),
                    0 0 0 1px rgba(99, 102, 241, 0.1);
    }}
    .module-card .module-num {{
        position: absolute;
        top: 14px;
        right: 18px;
        font-size: 2.2rem;
        font-weight: 900;
        color: rgba(148, 163, 184, 0.08);
        line-height: 1;
    }}

    /* ── How-to-Use Guide Panel ── */
    .guide-step {{
        background: rgba(30, 41, 59, 0.35);
        border-left: 3px solid {COLOR_ACCENT_PRIMARY};
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin-bottom: 10px;
        transition: border-color 0.3s ease, background 0.3s ease;
    }}
    .guide-step:hover {{
        border-left-color: {COLOR_ACCENT_SECONDARY};
        background: rgba(30, 41, 59, 0.5);
    }}
    .guide-step-num {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 26px;
        height: 26px;
        background: {COLOR_ACCENT_PRIMARY};
        color: #090D16;
        font-weight: 800;
        font-size: 0.78rem;
        border-radius: 50%;
        margin-right: 10px;
    }}

    /* ── Tabs Styling ── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{
        width: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: {COLOR_BG};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {COLOR_BORDER};
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLOR_TEXT_MUTED};
    }}

    /* ── Links ── */
    a {{
        color: {COLOR_ACCENT_SECONDARY};
        text-decoration: none;
        transition: color 0.2s ease;
    }}
    a:hover {{
        color: #A78BFA;
    }}

    /* ── Selection ── */
    ::selection {{
        background: rgba(99, 102, 241, 0.3);
        color: {COLOR_TEXT_LIGHT};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
