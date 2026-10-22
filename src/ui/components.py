"""
AAYAM - Reusable UI Components
Standardized cards, headers, alert boxes, provenance footers, and navigation blocks.
"""
import streamlit as st
from src.utils.config import APP_NAME, APP_TAGLINE, SDG_ALIGNMENT


def render_header(title: str, subtitle: str, badge_text: str | None = None, badge_type: str = "emerald"):
    """Render consistent page header with metadata badge and description."""
    badge_html = ""
    if badge_text:
        badge_html = f'<span class="badge badge-{badge_type}">{badge_text}</span>'
        
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
                <h1 style="margin: 0; font-size: 2.1rem; font-weight: 700; color: #F8FAFC;">{title}</h1>
                {badge_html}
            </div>
            <p style="margin: 0; font-size: 1.05rem; color: #94A3B8;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_kpi_card(title: str, value: str, subtext: str = "", delta_text: str = "", badge_color: str = "emerald"):
    """Render a styled fintech KPI card inside a Streamlit column."""
    delta_html = ""
    if delta_text:
        delta_html = f'<div style="margin-top: 6px;"><span class="badge badge-{badge_color}">{delta_text}</span></div>'
        
    st.markdown(
        f"""
        <div class="kpi-container">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtext">{subtext}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_alert_box(title: str, message: str, alert_type: str = "info"):
    """
    Render a styled alert banner.
    alert_type: 'info', 'warning', 'danger', 'success'
    """
    colors = {
        "info": ("rgba(99, 102, 241, 0.15)", "#818CF8", "ℹ️"),
        "success": ("rgba(16, 185, 129, 0.15)", "#34D399", "✅"),
        "warning": ("rgba(245, 158, 11, 0.15)", "#FBBF24", "⚠️"),
        "danger": ("rgba(244, 63, 94, 0.15)", "#FB7185", "🚨")
    }
    bg, fg, icon = colors.get(alert_type, colors["info"])
    
    st.markdown(
        f"""
        <div style="background-color: {bg}; border-left: 4px solid {fg}; padding: 14px 18px; border-radius: 6px; margin: 12px 0;">
            <div style="font-weight: 600; color: {fg}; font-size: 0.92rem; margin-bottom: 4px;">{icon} {title}</div>
            <div style="color: #F8FAFC; font-size: 0.85rem; line-height: 1.4;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_data_provenance(dataset_name: str, publisher: str, reference_period: str, source_url: str):
    """Render source transparency note indicating data origin and verification."""
    st.markdown(
        f"""
        <div class="provenance-box">
            <strong>Data Provenance:</strong> {dataset_name} &bull; 
            <strong>Publisher:</strong> {publisher} &bull; 
            <strong>Period:</strong> {reference_period} &bull; 
            <a href="{source_url}" target="_blank" style="color: #818CF8; text-decoration: none;">[Official Source ↗]</a>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_empty_state(message: str, action_text: str | None = None, target_page: str | None = None):
    """Render empty or unconfigured state with guidance."""
    st.markdown(
        f"""
        <div class="aayam-card" style="text-align: center; padding: 36px 20px;">
            <div style="font-size: 2rem; margin-bottom: 12px;">📊</div>
            <h3 style="color: #F8FAFC; margin-bottom: 8px;">No Profile Data Configured</h3>
            <p style="color: #94A3B8; font-size: 0.92rem; max-width: 500px; margin: 0 auto 16px auto;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if action_text and target_page:
        if st.button(action_text):
            st.switch_page(target_page)


def render_footer():
    """Render student prototype disclaimer and SDG mission footer."""
    st.markdown(
        f"""
        <div class="aayam-footer">
            <strong>{APP_NAME}</strong> — {APP_TAGLINE}<br>
            Student Decision-Support Prototype for Academic & Research Evaluation &bull;
            Aligned with <strong>{SDG_ALIGNMENT[0]}</strong> and <strong>{SDG_ALIGNMENT[1]}</strong>.<br>
            <em>Notice: AAYAM is an educational decision-support prototype. It does not provide certified financial, legal, credit, or banking advice.</em>
        </div>
        """,
        unsafe_allow_html=True
    )
